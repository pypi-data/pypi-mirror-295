import os
import re
import boto3
import botocore
from cloudpathlib import CloudPath, S3Client


class StorageUtils:
    def __init__(self, config_boto, config_cloudpath):
        self.resource = boto3.resource("s3", **config_boto)
        self.clientS3 = S3Client(**config_cloudpath)

    def get_cloud_path(self, bucket_name: str, folder: str, file: str):
        if folder is None and bucket_name is not None:
            return CloudPath("s3://" + bucket_name, client=self.clientS3)
        elif folder is not None:
            return CloudPath("s3://" + bucket_name + "/" + folder, client=self.clientS3)
        elif file is not None:
            return CloudPath(file, client=self.clientS3)

    def list_bucket(self, bucket: str) -> list[str]:
        return [obj for obj in self.resource.Bucket(bucket).objects.all()]

    def download_file_locally(self, bucket: str, filename: str):
        try:
            self.resource.Bucket(bucket).download_file(filename, "./" + re.sub('.*/', '', filename))
        except botocore.exceptions.ClientError:
            raise FileNotFoundError(
                f"File {filename} cannot be found in bucket {bucket}"
            )

    def upload(self, bucket: str, filepath: str):
        _, filename = os.path.split(filepath)

        self.resource.Bucket(bucket).upload_file(Filename=filepath, Key=filename)
