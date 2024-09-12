# Data utilities for EO4EU

This package provides classes and functions that help with common tasks involving:

- Reading data from configMaps and secrets
- Uploading to and downloading from S3 buckets
- Configuring components in general

## Installation

`eo4eu-data-utils` is published on [PyPI](https://pypi.org/project/eo4eu-data-utils/) and can be installed with `pip` anywhere. You can look for the latest version and pin that in your `requirements.txt` or what-have-you.

## Usage

For example usage of this package, you may refer to [post-pro](https://git.apps.eo4eu.eu/eo4eu/eo4eu-provision-handler/post-pro), [jupyter-openfaas](https://git.apps.eo4eu.eu/eo4eu/eo4eu-openfaas-operations/jupyter-openfaas) or [jupyter-proxy](https://git.apps.eo4eu.eu/eo4eu/eo4eu-openfaas-operations/jupyter-proxy).

### ConfigMaps and Secrets

The new API is very similar to the old one:

```py
from eo4eu_data_utils.access import ClusterAccess

access = ClusterAccess()

BOTO_CONFIG = {
    "region_name":           access.cfgmap("s3-access", "region_name"),
    "endpoint_url":          access.cfgmap("s3-access", "endpoint_url"),
    "aws_access_key_id":     access.secret("s3-access-scr", "aws_access_key_id"),
    "aws_secret_access_key": access.secret("s3-access-scr", "aws_secret_access_key"),
}
```

For testing purposes, you may also use the `ClusterAccess.mock` constructor, providing a `json` file with all the relevant values:

```py
access = ClusterAccess.mock("tests/config.json")
```

For the above example, the `json` file needs to have the following structure:

```json
{
    "/configmaps": {
        "s3-access/region_name": "...",
        "s3-access/endpoint_url": "..."
    },
    "/secrets": {
        "s3-access-scr/aws_access_key_id": "...",
        "s3-access-scr/aws_secret_access_key": "..."
    }
}
```

If you need something like that, it is recommended that you not use this, but instead the config utilities described below.

### S3 Access

The old `StorageUtils` class is supported:

```py
from eo4eu_data_utils.legacy import StorageUtils

ap = StorageUtils(config_boto=CONFIG_BOTO, config_cloudpath=CONFIG_CLOUD)
```

But the new one is more convenient; you specify the bucket when creating it and you don't have to keep track of it for every call:

```py
from eo4eu_data_utils.storage import Datastore

datastore = Datastore(
    config = CONFIG_BOTO,  # exactly the same config dict as before
    bucket = BUCKET_NAME
)
```

List files in bucket:

```py
files = datastore.list_files(subfolder, subsubfolder, ...)  # paths for (nested) subfolders are optional
```

Download and upload bytes:

```py
file_data = datastore.download(s3_key)
succeeded: bool = datastore.upload(other_s3_key, file_data)
```

Download and upload files:

```py
dl_succeeded: bool = datastore.download_to(s3_key, local_path)
up_succeeded: bool = datastore.upload_from(local_path, s3_key)
```

Download and upload many files at once:

```py
dl_s3_keys = ["data/d0.csv", "data/d1.csv", "data/img.tiff"]
dl_output_dir = "download_dir"
dl_result = datastore.download_many(dl_s3_keys, dl_output_dir)

up_s3_keys = ["output/result_0/meta.json", "output/result_0/r0.csv"]
up_input_dir = "output"
up_result = datastore.upload_many(up_s3_keys, up_input_dir)
```

Here the variables `dl_result` and `up_result` are of the class `eo4eu_data_utils.storage.TransferResult` and contain the succeeded and failed transfers. Example:

```py
for success in dl_result.succeeded:
    logger.info(f"Downloaded {success.src} to {success.dst}")

for failure in dl_result.failed:
    logger.warning(f"Failed to download {failure.src} to {failure.dst}")
```

You can check the number of successses/failures by way of `TransferResult.succeeded_num` and `TransferResult.failed_num`, or just get the `len` of the above lists.


### Configuration

The `Config` class allows you to define a configuration dict and fill it in different ways depending on whether you're on dev or prod. For example:

```py
from eo4eu_data_utils.config import Config, Wants

unfilled_config = Config(
    boto = {
        "region_name":           Wants.cfgmap("s3-access", "region_name"),
        "endpoint_url":          Wants.cfgmap("s3-access", "endpoint_url"),
        "aws_access_key_id":     Wants.secret("s3-access-scr", "aws_access_key_id"),
        "aws_secret_access_key": Wants.secret("s3-access-scr", "aws_secret_access_key"),
    },
    eo4eu = {
        "namespace":      Wants.cfgmap("eo4eu", "namespace"),
        "s3_bucket_name": Wants.cfgmap("eo4eu", "s3-bucket-name"),
    },
    # ...
)
```

The values may be accessed as nested attributes or dict items:

```py
# all of these are valid
key_id = config.boto.aws_access_key_id
key_id = config.boto["aws_access_key_id"]
key_id = config["boto"].aws_access_key_id
key_id = config["boto"]["aws_access_key_id"]
```

This means that `config.boto` is *not* a python dict. If you need a dict, you can convert it like so:

```py
client = boto3.client(**config.boto.to_dict())
```

### Filling the configuration

On prod, you can fill an unfilled config from the configMaps and secrets on the cluster:

```py
config = unfilled_config.fill_from_store()
```

On dev, you can fill it from environment variables:

```py
config = unfilled_config.fill_from_env()
```

For the previous example, the environment variables must be of the form:
```sh
export CONFIGMAPS_S3_ACCESS_REGION_NAME=
export CONFIGMAPS_S3_ACCESS_ENDPOINT_URL=
export CONFIGMAPS_EO4EU_NAMESPACE=
export CONFIGMAPS_EO4EU_S3_BUCKET_NAME=

export SECRETS_S3_ACCESS_SCR_AWS_ACCESS_KEY_ID=
export SECRETS_S3_ACCESS_SCR_AWS_SECRET_ACCESS_KEY=
```

Or, you can fill it from a json file:
```py
config = unfilled_config.fill_from_json("path_to/config.json")
```

Which must have the following format:

```json
{
    "configmaps": {
        "s3-access": {
            "region_name": "",
            "endpoint_url": ""
        },
        "eo4eu": {
            "namespace": "",
            "s3-bucket-name": ""
        }
    },
    "secrets": {
        "s3-access-scr": {
            "aws_access_key_id": "",
            "aws_secret_access_key": ""
        }
    }
}
```

Though it is recommended that you do this with environment variables.

Some common configs are defined in [eo4eu_data_utils.config](https://git.apps.eo4eu.eu/eo4eu/eo4eu-provision-handler/eo4eu-data-utils/-/blob/main/eo4eu_data_utils/config.py), you may want to take a look at them.

You can automatically convert the `Wants` values to different types and set default values to be used in case they are not found:

```py
from eo4eu_data_utils.config import Config, Wants
from pathlib import Path

unfilled_config = Config(
    # ...
    elasticsearch = {
        "username": Wants.secret("els-access-scr", "username"),
        "password": Wants.secret("els-access-scr", "password"),
        "local_dir": Wants.cfgmap("els", "local").to(Path).with_default("els_dir"),
        "max_retries": Wants.cfgmap("els", "max_retries").to(int).with_default(10)
    }
)
```

A third constructor for `Wants` is provided: `Wants.option`. This is different to `cfgmap` and `secret` in that it's not automatically filled by the cluster storage, but it can be filled using the other methods. It's there to provide extra configuration, for example:

```py
from eo4eu_data_utils.config import Config, Wants

unfilled_config = Config(
    # ...
    testing = {
        "raise_exceptions": Wants.option("debug", "raise_exceptions").to_bool().with_default(False),
        "max_retries":      Wants.option("http", "max_retries").to_int().with_default(5),
    },
)
```

These can be filled from a json file:

```py
config = unfilled_config.fill_from_json("path_to/config.json")
```

Which has the form:

```json
{
    ...
    "debug": {
        "raise_exceptions": true 
    },
    "http": {
        "max_retries": 10
    }
}
```

Or directly from a python dictionary:

```py
config = unfilled_config.fill_from_dict({
    "debug": { "raise_exceptions": True },
    "http": { "max_retries": 10 },
})
```

Or from environment variables:

```py
config = unfilled_config.fill_from_env()
```

With:

```sh
export DEBUG_RAISE_EXCEPTIONS=true
export HTTP_MAX_RETRIES=10
```
