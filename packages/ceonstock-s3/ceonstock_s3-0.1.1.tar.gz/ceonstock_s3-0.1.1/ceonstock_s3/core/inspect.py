# Information about the files in s3.
# These functions do not modify the files in any way.
import logging
from .base import s3_resource

logger = logging.getLogger(__name__)


def list_s3_files(bucket_name, remote_dir):
    # TODO is recursive?
    logger.debug(f"Listing s3 bucket({bucket_name}) files in dir {remote_dir}:")
    bucket = s3_resource.Bucket(bucket_name)
    remote_file_list = []
    try:
        objects = bucket.objects.filter(Prefix=remote_dir)
    except Exception as e:
        logger.error(f"Failed to list_s3_files in s3: {e}")
        raise e
    logger.debug(f"Found objects: {objects}")
    for obj in objects:
        remote_file_list.append(obj.key)
    logger.debug(f"remote_file_list: {remote_file_list}")
    return remote_file_list


# A recursive version adapted from "download folder"
def get_file_list(bucket_name, s3_folder):
    logger.debug(f"Listing s3 bucket({bucket_name}) files in dir {s3_folder}...")
    file_list = []
    bucket = s3_resource.Bucket(bucket_name)
    try:
        objects = bucket.objects.filter(Prefix=s3_folder)
    except Exception as e:
        logger.error(f"Failed to get_file_list in s3: {e}")
        raise e
    for obj in objects:
        if obj.key[-1] == "/":
            continue
        # Add key to list
        file_list.append(obj.key)
    logger.debug(f"... Got file_list: {file_list}")
    return file_list


def check_for_expected_files_in_s3(bucket_name, remote_dir, expected_files):
    """Returns an object containing lists of found and missing files"""
    logger.debug(f"Got expected_files: {expected_files}")
    remote_file_list = list_s3_files(bucket_name, remote_dir)
    logger.debug(f"Got remote_file_list: {remote_file_list}")

    files_found = []
    files_missing = []
    files_anomaly = []
    for file in expected_files:
        logger.debug(f"file: {file}")
        if file in remote_file_list:
            files_found.append(file)
        else:
            files_missing.append(file)
    for file in remote_file_list:
        if file not in expected_files:
            files_anomaly.append(file)
    remote_file_check = {
        "found": files_found,
        "missing": files_missing,
        "anomaly": files_anomaly,
    }
    logger.debug(f"Returning remote_file_check: {remote_file_check}")
    return remote_file_check
