import json
import logging
from pathlib import Path
from typing import Self


class ClusterAccess:
    def __init__(
        self,
        logger = None,
        configmap_dir: str|Path = "/configmaps",
        secret_dir: str|Path = "/secrets"
    ):
        if logger is None:
            logger = logging.getLogger(__name__)
        self.logger = logger

        self.configmap_dir = Path(configmap_dir)
        self.secret_dir = Path(secret_dir)
        self._cache = {}

    # fill cfgmaps and secrets manually for testing purposes
    # using a json file that is not commited to source control
    @classmethod
    def mock(cls, config_path: str|Path, **kwargs) -> Self:
        result = ClusterAccess(**kwargs)
        config = json.loads(Path(config_path).read_text())

        for directory, file_dict in config.items():
            dir_path = Path(directory)
            for path, content in file_dict.items():
                path_str = str(dir_path.joinpath(path))
                result._cache[path_str] = content

        return result

    def _get(self, name: str, path: str|Path) -> str:
        path_str = str(path)
        if path_str in self._cache:
            return self._cache[path_str]

        try:
            result = Path(path).read_text()
            self._cache[path_str] = result
            return result
        except Exception as e:
            self.logger.error(f"Unable to read {name} in {path_str}: {e}")
            return ""

    def cfgmap(self, *paths: str|Path) -> str:
        return self._get("ConfigMap", self.configmap_dir.joinpath(*paths))

    def secret(self, *paths: str|Path) -> str:
        return self._get("Secret", self.secret_dir.joinpath(*paths))

