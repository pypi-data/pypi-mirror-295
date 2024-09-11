import logging

# from botocore.exceptions import ClientError, ConnectionClosedError
# from app import errors

from .base import s3_client, s3_resource
from botocore.exceptions import ClientError, ConnectionClosedError

logger = logging.getLogger(__name__)


def create_get(bucket_name, object_key, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    # s3_client = boto3.client("s3")
    logger.debug(f"Getting bucket({bucket_name}) key: {object_key}")
    try:
        response = s3_client.generate_presigned_url(
            "get_object",  # or other s3 commands
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=expiration,
        )
    except ClientError as e:
        logger.error(f"Failed to create presigned get url for {object_key}")
        raise e

    # The response contains the presigned URL
    return response


def create_post(
    bucket_name, object_name, fields=None, conditions=None, expiration=3600
):
    """Generate a presigned URL S3 POST request to upload a file

    :param bucket_name: string
    :param object_name: string
    :param fields: Dictionary of prefilled form fields
    :param conditions: List of conditions to include in the policy
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """

    # Generate a presigned S3 POST URL
    # s3_client = boto3.client("s3")
    try:
        response = s3_client.generate_presigned_post(
            bucket_name,
            object_name,
            Fields=fields,
            Conditions=conditions,
            ExpiresIn=expiration,
        )
    except ClientError as e:
        logger.error(
            f"Failed to create presigned post for ({bucket_name}) {object_name}"
        )
        raise e
    # The response contains the presigned URL and required fields
    return response


"""
def upload_to_presigned_post(response, file_path):
    # Demonstrate how another Python program can use the presigned URL to upload a file
    with open(file_path, "rb") as f:
        files = {"file": (file_path, f)}
        http_response = requests.post(
            response["url"], data=response["fields"], files=files
        )
    # If successful, returns HTTP status code 204
    print(f"File upload HTTP status code: {http_response.status_code}")

# TODO implement (current ver is placeholder from:
# https://stackoverflow.com/questions/44978426/boto3-file-upload-does-it-check-if-file-exists
# Check for more modern workflow?
# def check(s3_service, bucket, key):
# from botocore.exceptions import ClientError
# try:
# s3_service.Object(bucket, key).load()
# except ClientError as e:
# return int(e.response['Error']['Code']) != 404
# return True
# print(check(s3_service, <bucket>, <key>))
"""
