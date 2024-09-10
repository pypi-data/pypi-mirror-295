import os
import json
import copy
import logging
from pprint import pformat
from pathlib import Path
from typing import Self, Any, Iterator
from enum import Enum

from .access import ClusterAccess


def _to_bool(input) -> bool:
    if isinstance(input, bool):
        return input
    if isinstance(input, str):
        input_lower = input.lower()
        if input_lower == "true" or input_lower == "1":
            return True
        else:
            return False
    if isinstance(input, int):
        return False if input == 0 else True
    return False


class WantKind(Enum):
    CFGMAP = "configMap"
    SECRET = "secret"
    OPTION = "option"


class Wants:
    def __init__(self, kind, *paths):
        self.kind = kind
        self.paths = list(paths)
        self.logger = None
        self.converter = lambda x: x
        self.has_default = False
        self.default = None

    @classmethod
    def cfgmap(self, *paths):
        return Wants(WantKind.CFGMAP, *paths)

    @classmethod
    def secret(self, *paths):
        return Wants(WantKind.SECRET, *paths)

    @classmethod
    def option(self, *paths):
        return Wants(WantKind.OPTION, *paths)

    def set_logger(self, logger) -> Self:
        self.logger = logger
        return self

    def append(self, suffix) -> Self:
        self.converter = lambda s: s + suffix
        return self

    def to(self, converter) -> Self:
        self.converter = converter
        return self

    def to_int(self) -> Self:
        return self.to(int)

    def to_bool(self) -> Self:
        return self.to(_to_bool)

    def with_default(self, val: Any) -> Self:
        self.has_default = True
        self.default = val
        return self

    def __add__(self, other) -> Self:
        return self.append(other)

    def __repr__(self) -> str:
        prefix = self._get_prefix(cfgmap = "cfgmap", secret = "secret", option = "option")
        args = ", ".join([str(path) for path in self.paths])
        return f"Wants.{prefix}({args})"

    def _get_prefix(self, extra_prefix: str = "", cfgmap = "configmaps", secret = "secrets", option = "") -> str:
        if self.kind == WantKind.CFGMAP:
            return f"{extra_prefix}{cfgmap}"
        if self.kind == WantKind.SECRET:
            return f"{extra_prefix}{secret}"
        if self.kind == WantKind.OPTION:
            return option

    def _fill_paths(self, filler_func) -> Self:
        return [
            filler_func(path) if isinstance(path, self.__class__) else path
            for path in self.paths
        ]

    def _return(self, val):
        try:
            return self.converter(val)
        except Exception as e:
            self.logger.warning(f"Could not convert {val}:\n{e}")
            return val

    def _bad_return(self, message: str, should_raise: bool = False) -> Self|Any:
        if self.has_default:
            return self._return(self.default)
        if should_raise:
            raise ValueError(message)
        self.logger.warning(message)
        return self

    def fill_from_store(self, access: ClusterAccess, raise_on_bad_return = False) -> Self|Any:
        paths = self._fill_paths(lambda path: path.fill_from_store(access))
        if self.kind == WantKind.CFGMAP:
            return self._return(access.cfgmap(*paths))
        if self.kind == WantKind.SECRET:
            return self._return(access.secret(*paths))
        else:
            return self._bad_return(
                f"Cannot fill Wants object of type \"{self.kind.value}\" from store",
                should_raise = raise_on_bad_return
            )

    def fill_from_env(self, raise_on_bad_return = False) -> Self|Any:
        paths = self._fill_paths(lambda path: path.fill_from_env())

        prefix = self._get_prefix().upper()
        env_var = "_".join([prefix] + [str(path).upper().replace("-", "_") for path in paths])

        try:
            return self._return(os.environ[env_var])
        except Exception as e:
            return self._bad_return(
                f"Could not find environment variable {env_var}:\n{e}",
                should_raise = raise_on_bad_return
            )

    def fill_from_dict(self, paths_dict: dict[str,Any], raise_on_bad_return = False) -> Self|Any:
        paths = self._fill_paths(lambda path: path.fill_from_dict(paths_dict))
        prefix = self._get_prefix()
        if prefix != "":
            paths = [prefix] + paths

        try:
            result = copy.deepcopy(paths_dict)
            for path in paths:
                result = result[path]

            return self._return(result)
        except Exception as e:
            self_path = Path(paths[0]).joinpath(*paths[1:])
            return self._bad_return(
                f"Could not find {self_path}:\n{e}",
                should_raise = raise_on_bad_return
            )


class Config:
    def __init__(self, **kwargs):
        self._logger = logging.getLogger(__name__)
        self._attrs = {
            Config(**val) if isinstance(val, dict) else val
            for key, val in kwargs.items()
        }
        self._attrs = {}
        for key, val in kwargs.items():
            if isinstance(val, dict):
                val = Config(**val)
            if isinstance(val, Config) or isinstance(val, Wants):
                val.set_logger(self._logger)

            self._attrs[key] = val

    @classmethod
    def from_dict(self, items: dict) -> Self:
        return Config(**items)

    def to_dict(self):
        return {
            key: val.to_dict() if isinstance(val, self.__class__) else val
            for key, val in self.items()
        }

    def extend(self, other: Self) -> Self:
        if isinstance(other, dict):
            other = Config.from_dir(other)
        self._attrs = self._attrs | other._attrs
        return self

    def __getattr__(self, key: str):
        if key[0] == "_":
            return super().__getattr__(key)
        return self._attrs[key]

    def __setattr__(self, key: str, val):
        if key[0] == "_":
            return super().__setattr__(key, val)
        self._attrs[key] = val

    def __getitem__(self, key: str):
        return self._attrs[key]

    def __setitem__(self, key: str, val):
        self._attrs[key] = val

    def __repr__(self) -> str:
        return pformat(self.to_dict())

    def items(self) -> Iterator[tuple[str,Any]]:
        return self._attrs.items()

    def set_logger(self, logger) -> Self:
        self._logger = logger
        return self

    def get_nested(self, keys: list[str]):
        head, tail = keys[0], keys[1:]
        if len(tail) == 0:
            return self[head]

        return self[head].get_nested(tail)

    def set_nested(self, keys: list[str], val):
        head, tail = keys[0], keys[1:]
        if len(tail) == 0:
            self[head] = val
        else:
            self[head].set_nested(tail, val)

    def _fill(self, filler_func) -> Self:
        result = Config()
        for key, val in self.items():
            result[key] = val
            if isinstance(val, self.__class__) or isinstance(val, Wants):
                result[key] = filler_func(val)
        return result

    def fill_from_store(self, access: ClusterAccess|None = None, **kwargs) -> Self:
        if access is None:
            access = ClusterAccess()
        return self._fill(lambda val: val.fill_from_store(access, **kwargs))

    def fill_from_env(self, **kwargs) -> Self:
        return self._fill(lambda val: val.fill_from_env(**kwargs))

    def fill_from_dict(self, paths: dict[str,Any], **kwargs) -> Self:
        return self._fill(lambda val: val.fill_from_dict(paths, **kwargs))

    def fill_from_json(self, message: str, **kwargs) -> Self:
        return self.fill_from_dict(json.loads(message), **kwargs)

    def fill_from_file(self, path: str|Path, **kwargs) -> Self:
        return self.fill_from_json(Path(path).read_text(), **kwargs)

    def fill_from_args(self, args: list[str], **kwargs) -> Self:
        paths = {}
        for arg in args:
            if "=" not in arg:
                continue
            key, val = arg.split("=")
            paths[key] = val

        return self.fill_from_dict(paths, **kwargs)

    def override_from_args(self, args: list[str]) -> Self:
        for arg in args:
            if "=" not in arg:
                continue
            key, val = arg.split("=")
            keys = key.split("/")
            try:
                self.set_nested(keys, val)
            except Exception as e:
                self._logger.warning(f"Could not set the value of key {key}:\n{e}")

        return self


default_kafka_consumer_config = Config.from_dict({
    "bootstrap.servers": Wants.cfgmap("kafka", "internal_bootstrap_servers"),
    "client.id": "eo4eu",
    "api.version.fallback.ms": 0,
    "group.id": "eo4eu",
    'enable.auto.commit': False,
    "auto.offset.reset": "latest",
})

default_kafka_producer_config = Config.from_dict({
    "bootstrap.servers": Wants.cfgmap("kafka", "internal_bootstrap_servers"),
    "client.id": "eo4eu",
    "api.version.fallback.ms": 0,
})

default_boto_config = Config.from_dict({
    "region_name":           Wants.cfgmap("s3-access", "region_name"),
    "endpoint_url":          Wants.cfgmap("s3-access", "endpoint_url"),
    "aws_access_key_id":     Wants.secret("s3-access-scr", "aws_access_key_id"),
    "aws_secret_access_key": Wants.secret("s3-access-scr", "aws_secret_access_key"),
})

default_cloud_config = Config.from_dict({
    "endpoint_url":          Wants.cfgmap("s3-access", "endpoint_url"),
    "aws_access_key_id":     Wants.secret("s3-access-scr", "aws_access_key_id"),
    "aws_secret_access_key": Wants.secret("s3-access-scr", "aws_secret_access_key"),
})

default_eo4eu_config = Config.from_dict({
    "namespace":      Wants.cfgmap("eo4eu", "namespace"),
    "s3_bucket_name": Wants.cfgmap("eo4eu", "s3-bucket-name"),
})
