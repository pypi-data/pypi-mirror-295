import boto3
from typing import Any
from pathlib import Path
from cloudpathlib import CloudPath, S3Client


def _make_callback(callback):
    if callback is None:
        return lambda s: s
    return callback


def _make_error_callback(callback):
    if callback is None:
        return lambda s, e: s
    return callback


class TransferEvent:
    def __init__(self, src: str, dst: str, info: Any):
        self.src = src
        self.dst = dst
        self.info = info


class TransferResult:
    def __init__(
        self,
        succeeded: list[TransferEvent]|None = None,
        failed: list[TransferEvent]|None = None,
    ):
        if succeeded is None:
            succeeded = []
        self.succeeded = succeeded
        if failed is None:
            failed = []
        self.failed = failed

    def succeeded_num(self) -> int:
        return len(self.succeeded)

    def failed_num(self) -> int:
        return len(self.failed)

    def total_num(self) -> int:
        return self.succeeded_num() + self.failed_num()

    def succeeded_src(self):
        return [event.src for event in self.succeeded]

    def succeeded_dst(self):
        return [event.dst for event in self.succeeded]

    def add(self, success: bool, event: TransferEvent):
        if success:
            self.succeeded.append(event)
        else:
            self.failed.append(event)


class Datastore:
    def __init__(
        self,
        config: dict[str,str],
        bucket: str,
        download_callback = None,
        download_error_callback = None,
        upload_callback = None,
        upload_error_callback = None
    ):
        self.resource = boto3.resource("s3", **config)
        self.bucket = self.resource.Bucket(bucket)
        self.bucket_name = bucket
        self.bucket_path = CloudPath(
            f"s3://{bucket}",
            client = S3Client(
                aws_access_key_id = config["aws_access_key_id"],
                aws_secret_access_key = config["aws_secret_access_key"],
                endpoint_url = config["endpoint_url"],
            )
        )
        self.download_callback = _make_callback(download_callback)
        self.upload_callback = _make_callback(upload_callback)
        self.download_error_callback = _make_error_callback(download_error_callback)
        self.upload_error_callback = _make_error_callback(upload_error_callback)

    def path(self, *paths) -> CloudPath:
        return self.bucket_path.joinpath(*paths)

    def list_files(self, *paths) -> list[str]:
        return [
            str(path.relative_to(self.bucket_path))
            for path in self.path(*paths).rglob("*")
            if path.is_file()
        ]

    def download(self, key: str|Path) -> bytes|None:
        key_str = str(key)
        self.download_callback(key_str)
        try:
            result = self.resource.Object(self.bucket_name, key_str).get()["Body"].read()
            return result
        except Exception as e:
            self.download_error_callback(key_str, e)
            return None

    def download_to(self, key: str|Path, local_path: str|Path) -> bool:
        key_str = str(key)
        self.download_callback(key_str)
        try:
            local_path = Path(local_path)
            local_path.parent.mkdir(parents = True, exist_ok = True)
            self.bucket.download_fileobj(key_str, local_path.open("wb"))
            return True
        except Exception as e:
            self.download_error_callback(key_str, e)
            return False

    def upload(self, key: str|Path, data: bytes) -> bool:
        key_str = str(key)
        self.upload_callback(key_str)
        try:
            self.bucket.put_object(Key = key_str, Body = data)
            return True
        except Exception as e:
            self.upload_error_callback(key_str, e)
            return False

    def upload_from(self, local_path: str|Path, key: str|Path) -> bool:
        key_str = str(key)
        self.upload_callback(key_str)
        try:
            self.bucket.upload_file(str(local_path), key_str)
            return True
        except Exception as e:
            self.upload_error_callback(key_str, e)
            return False

    def download_many(self,
        keys: list[str|Path],
        output_dir: str|Path,
        input_dir: str|Path = "",
        extra_info: list[Any]|None = None
    ) -> TransferResult:
        if extra_info is None:
            extra_info = [None for _ in range(len(keys))]

        output_path = Path(output_dir)
        result = TransferResult()
        for key, info in zip(keys, extra_info):
            src, dst = key, key
            success = False
            try:
                src, dst = key, output_path.joinpath(Path(key).relative_to(input_dir))
                success = self.download_to(src, dst)
            except Exception as e:
                self.download_callback(key)
                self.download_error_callback(key, e)

            event = TransferEvent(src, dst, info)
            result.add(success, event)

        return result

    def upload_many(self,
        keys: list[str|Path],
        input_dir: str|Path,
        output_dir: str|Path = "",
        extra_info: list[Any]|None = None
    ) -> TransferResult:
        if extra_info is None:
            extra_info = [None for _ in range(len(keys))]

        output_path = Path(output_dir)
        result = TransferResult()
        for key, info in zip(keys, extra_info):
            src, dst = key, key
            success = False
            try:
                src, dst = key, output_path.joinpath((Path(key).relative_to(input_dir)))
                success = self.upload_from(src, dst)
            except Exception as e:
                self.upload_callback(key)
                self.upload_error_callback(key, e)

            event = TransferEvent(src, dst, info)
            result.add(success, event)

        return result
