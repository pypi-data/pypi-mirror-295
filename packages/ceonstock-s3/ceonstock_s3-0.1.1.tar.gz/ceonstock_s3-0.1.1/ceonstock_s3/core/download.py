import os
import logging

from .base import s3_resource

logger = logging.getLogger(__name__)

from botocore.exceptions import ClientError, ConnectionClosedError


def file(bucket_name, remote_file_path, local_file_path=None, overwrite=False):
    if not local_file_path:
        logger.warn(
            f"local_file_path not given. Matching remote_file_path: {remote_file_path}"
        )
        local_file_path = remote_file_path
    logger.debug(f"Starting download ({bucket_name}){remote_file_path} as {local_file_path} ...")
    already_exists = os.path.isfile(local_file_path)
    if not already_exists or overwrite:
        overwrite_msg = "(OVERWRITE) " if already_exists else ""
        logger.info(
            f"Downloading ({bucket_name}){remote_file_path} as {overwrite_msg}{local_file_path}..."
        )
        try:
            s3_resource.Object(bucket_name, remote_file_path).download_file(
                f"{local_file_path}"
            )
        except ClientError as e:
            logger.warn(f"Caught ClientError: {e}")
            if e.response["ResponseMetadata"]["HTTPStatusCode"] == 404:
                logger.error(
                    f"File not found in s3: ({bucket_name}) {remote_file_path}"
                )
            else:
                logger.error(
                    f"Unknown ClientError Exception: {e}\nClientError e.response: {e.response}"
                )
            raise e
        except Exception as e:
            logger.error(f"Failed to download {remote_file_path} to {local_file_path}")
            raise e
    else:
        logger.warn(f"File {local_file_path} already exists! Skipping download...")
    return local_file_path


def folder(bucket_name, s3_folder, local_dir=None):
    """
    Download the contents of a folder directory
    Args:
        bucket_name: the name of the s3 bucket
        s3_folder: the folder path in the s3 bucket
        local_dir: a relative or absolute directory path in the local file system
    """
    bucket = s3_resource.Bucket(bucket_name)
    for obj in bucket.objects.filter(Prefix=s3_folder):
        target = (
            obj.key
            if local_dir is None
            else os.path.join(local_dir, os.path.relpath(obj.key, s3_folder))
        )
        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target))
        if obj.key[-1] == "/":
            continue
        logger.info(f"Downloading: {obj.key} to {target}")
        bucket.download_file(obj.key, target)
