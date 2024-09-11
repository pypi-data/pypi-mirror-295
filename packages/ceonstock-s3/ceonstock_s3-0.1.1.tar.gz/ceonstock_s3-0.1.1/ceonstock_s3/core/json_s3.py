import logging
import json

logger = logging.getLogger(__name__)

from .base import s3_client
from botocore.exceptions import ClientError, ConnectionClosedError
from ceonstock_s3 import errors


def read_json_as_dict(bucket_name, remote_file_key):
    logger.debug(f"Getting json from bucket({bucket_name}): {remote_file_key}")
    try:
        s3_clientobj = s3_client.get_object(
            Bucket=bucket_name, Key=remote_file_key
        )
    except ClientError as error:
        if error.response["Error"]["Code"] == "NoSuchKey":
            msg = (
                f"Key not found in s3 bucket({bucket_name}): {remote_file_key}"
            )
            logger.error(msg)
            raise errors.S3FileNotFoundError(
                bucket=bucket_name, key=remote_file_key
            )
        else:
            raise error
    s3_objdata = s3_clientobj["Body"].read().decode("utf-8")
    json_data = json.loads(s3_objdata)
    logger.debug(f"Got json data from {remote_file_key}: {json_data}")
    return json_data


def save_dict_as_json(bucket_name, dict_to_save, remote_file):
    """Receives a dict and saves it to a json file in s3"""
    logger.info(f"Saving json file to s3({bucket_name}){remote_file} ...")
    logger.debug(f"Got dict_to_save: {dict_to_save}")
    json_data = json.dumps(dict_to_save, indent=4)
    logger.info(f"Saving json string:\n{json_data}")
    try:
        response = s3_client.put_object(
            Bucket=bucket_name,
            Key=remote_file,
            Body=json_data,
        )
    except ConnectionClosedError as e:
        msg = f"Caught a ConnectionClosedError: Failed to upload json data to s3 {remote_file}."
        logger.error(msg)
        logger.error(
            "TODO: Implement retry for connection failures, manage proper logging behaviour"
        )
        raise e
    except Exception as e:
        msg = f"Failed to upload json data to s3 {remote_file}: {e}"
        logger.error(msg)
        raise e
    logger.debug(f"Succesfully uploaded json data to: {remote_file}")
    logger.debug(f"Received response: {response}")
    return True


def save_directly_as_json(bucket_name, json_data, remote_file):
    """Receives json data directly (skips json.dumps)"""
    logger.info(f"Uploading json file to {remote_file} ...")
    # json_data = json.dumps(dict_to_save, indent=4)
    logger.debug(f"Saving json_data: {json_data}")
    try:
        response = s3_client.put_object(
            Bucket=bucket_name,
            Key=remote_file,
            Body=json_data,
        )
    except ConnectionClosedError as e:
        msg = f"Caught a ConnectionClosedError: Failed to upload json data to s3 {remote_file}."
        logger.error(msg)
        logger.error(
            "TODO: Implement retry for connection failures, manage proper logging behaviour"
        )
        raise e
    except Exception as e:
        msg = f"Failed to upload json data to s3 {remote_file}: {e}"
        logger.error(msg)
        raise e
    logger.debug(f"Succesfully uploaded json data to: {remote_file}")
    logger.debug(f"Received response: {response}")
    return True
