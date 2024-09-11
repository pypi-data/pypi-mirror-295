import boto3  # boto3 automatically connects using credentials in ~/.aws/

# from botocore.exceptions import ClientError, ConnectionClosedError

# TODO error handling: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/error-handling.html
# from render.utility.log import get_job_logger

s3_client = boto3.client("s3")
s3_resource = boto3.resource("s3")
