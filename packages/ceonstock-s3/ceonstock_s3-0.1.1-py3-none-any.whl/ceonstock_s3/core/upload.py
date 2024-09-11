import logging
from typing import Union
from pathlib import Path

# from botocore.exceptions import ClientError, ConnectionClosedError
# from app import errors

from .base import s3_resource

logger = logging.getLogger(__name__)


def file(bucket_name: str, local_file: Union[str, Path], remote_file: str):
    logger.info(f"Uploading {local_file} as ({bucket_name}){remote_file}...")
    # my_bucket = s3_resource.Bucket(name=my_bucket_name)
    new_object = s3_resource.Object(bucket_name=bucket_name, key=remote_file)
    try:
        # Using 'client' to upload files rather than 'resource' might give a different
        # ..response?
        response = new_object.upload_file(str(local_file))
    # except ClientError as e:
    except Exception as e:
        msg = (
            f"Failed to upload {local_file} to s3 ({bucket_name}){remote_file}"
        )
        logger.error(msg)
        raise e
    logger.info(
        f"Succesfully uploaded: {local_file} as ({bucket_name}){remote_file}"
    )
    return remote_file
