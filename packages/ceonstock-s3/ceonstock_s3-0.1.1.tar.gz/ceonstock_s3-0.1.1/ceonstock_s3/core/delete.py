import logging
from .base import s3_resource

logger = logging.getLogger(__name__)


def file(bucket_name: str, object_key: str):
    """Delete a single s3 file.
    Return None if the object_key does not exist
    Returns the s3 response if delete() is submitted successfully"""
    obj = s3_resource.Object(bucket_name, object_key)
    logger.info(f"deleting obj: {obj.key}")
    # try:
    # test = obj.get()  # Download the object
    # except s3_resource.meta.client.exceptions.NoSuchKey as e:
    # test = "CAUGHT! obj.get()"
    # logger.warn(f"Caught NoSuchKey s3 exception: {e}")
    try:
        test = obj.load()  # Get just the headers of the object
        logger.info(f"TEST: {test}")
    except s3_resource.meta.client.exceptions.ClientError as e:
        return None
    obj.delete()
    return object_key


def folder(bucket_name: str, remote_dir: str):
    """Delete a folder.
    Folder_key should end with a trailing slash
    Returns a list of deleted object keys"""
    # s3 = boto3.resource('s3')
    bucket = s3_resource.Bucket(bucket_name)
    if not remote_dir.endswith("/"):
        remote_dir += "/"
    logger.info(f"Got DELETE request for bucket({bucket_name}) folder: {remote_dir}")
    s3_objects = bucket.objects.filter(Prefix=remote_dir)
    deleted_files = []
    for obj in s3_objects:
        deleted_files.append(obj.key)
    if not deleted_files:
        return []
    res = s3_objects.delete()
    # res = bucket.objects.filter(Prefix="myprefix/").delete()
    logger.info(f"Got res: {res}")
    return deleted_files
