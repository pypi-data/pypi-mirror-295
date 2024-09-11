# Information about the files in s3.
# These functions do not modify the files in any way.
import logging
from .base import s3_resource

logger = logging.getLogger(__name__)


def file(source_bucket: str, source_key: str, dest_key: str, dest_bucket=None):
    if not dest_bucket:
        dest_bucket = source_bucket
    copy_source = {"Bucket": source_bucket, "Key": source_key}
    logger.debug(
        f"Copying from ({source_bucket}){source_key} to ({dest_bucket}){dest_key}"
    )
    bucket = s3_resource.Bucket(dest_bucket)
    bucket.copy(copy_source, dest_key)
    logger.info(
        f"Copied s3 file from ({source_bucket}){source_key} to ({dest_bucket}){dest_key}"
    )
