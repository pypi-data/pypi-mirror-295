import json
from typing import Union
from typing import Dict
from typing import Optional
from uuid import UUID
from pathlib import Path
import logging

from . import core
from . import buckets

BUCKET_NAME = buckets.SUBMISSION

logger = logging.getLogger(__name__)

DEFAULT_JSON_FILE = "submission.json"


def save_json(
    submission_uuid: Union[UUID, str],
    json_dict_data: dict,
    bucket: str = BUCKET_NAME,
    json_file: str = DEFAULT_JSON_FILE,
) -> None:
    """Create the json file or overwrite it if it already exists"""
    json_file_key = f"{submission_uuid}/{json_file}"
    core.json_s3.save_dict_as_json(bucket, json_dict_data, json_file_key)
    return


def save_json_string(
    submission_uuid: Union[UUID, str],
    json_string: str,
    bucket: str = BUCKET_NAME,
    json_file: str = DEFAULT_JSON_FILE,
) -> None:
    """Create the json file or overwrite it if it already exists"""
    json_file_key = f"{submission_uuid}/{json_file}"
    core.json_s3.save_directly_as_json(bucket, json_string, json_file_key)
    return


def read_json(
    submission_uuid: Union[UUID, str],
    bucket: str = BUCKET_NAME,
    json_file: str = DEFAULT_JSON_FILE,
) -> dict:
    """Read the json file from the s3 bucket and return it as a dictionary"""
    json_file_key = f"{submission_uuid}/{json_file}"
    json_dict = core.json_s3.read_json_as_dict(bucket, json_file_key)
    logger.debug(f"Read json from s3({bucket}){json_file_key}:\n{json_dict}")
    return json_dict


def download_file(
    submission_uuid: Union[str, UUID],
    remote_file_path_relative: str,
    local_dir: Union[str, Path],
    bucket: str = BUCKET_NAME,
    rename: Optional[str] = None,
) -> Path:
    """
    Download a single file from the s3 submission directory.
    remote_file_path_relative: The remote key relative to the submission's root dir
    """
    submission_root_dir = str(submission_uuid)
    remote_file_path = f"{submission_root_dir}/{remote_file_path_relative}"
    file_name = Path(remote_file_path).name
    if rename:
        # Don't allow the extension to be changed by mistake: Explicitly preserve the
        # original filename's extension
        file_name = f"{Path(rename).stem}{Path(remote_file_path).suffix}"
    local_file_path = f"{local_dir}/{file_name}"
    if not Path(local_file_path).parent.exists():
        logger.warning(f"Creating dir: {Path(local_file_path).parent}")
        Path(local_file_path).parent.mkdir(parents=True, exist_ok=True)
    result = core.download.file(
        bucket_name=bucket,
        remote_file_path=remote_file_path,
        local_file_path=local_file_path,
    )
    logger.warning(f"submission downloaded result: {result}")
    return Path(result)


def upload_file(
    submission_uuid: Union[str, UUID],
    local_file_path: str,
    remote_dir: str = "",
    file_rename: Optional[str] = None,
    bucket: str = BUCKET_NAME,
) -> str:
    """
    Upload a single file from the local filesystem into the target remote dir.
    local_file_path: A path to the file in the local filesystem
    remote_dir: The remote dir to place the file into, relative to the submission's root dir
    file_rename: If provided, rename the file when uploading to s3.
    Returns: The s3 file key relative to the submissioin root dir
    """
    submission_root_dir = str(submission_uuid)
    file_name = file_rename if file_rename else Path(local_file_path).name
    # Convert to path to handle double backslashes in case remote_dir is empty
    remote_file_path = Path(f"{submission_root_dir}/{remote_dir}/{file_name}")
    # If no remote_dir is specified, avoid leading '/'
    submission_rel_file_path = (
        Path(f"{remote_dir}/{file_name}") if remote_dir else Path(file_name)
    )
    core.upload.file(
        bucket_name=bucket,
        local_file=local_file_path,
        remote_file=str(remote_file_path),
    )
    return str(submission_rel_file_path)


# A user-friendly interface to build the required args for generating presigned
# post urls for a submission file upload
def create_presigned_post(
    submission_uuid: Union[str, UUID],
    s3_relative_filepath: str,  # Filepaths relative to submssion dir
    s3_content_type: str = "/image",
    expiration=3600,  # TODO make units clearer
    bucket: str = BUCKET_NAME,
):
    """Generate a presigned URL S3 POST request to upload a file belonging to a submission.

    :param submission_uuid: The uuid of the submission that the file belongs to.
    :param s3_relative_filepath: The path to the file, relative to the submissions' root dir.
    :param s3_content_type: The (mime-type string?) of the content type. Used to generate upload conditions.
    :param bucket: string The s3 bucket to submit to.
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    """
    logger.debug(f"Got content_type: {s3_content_type}")
    # TODO stricter content-type checking (record content-type when uploaded)
    conditions = [
        ["content-length-range", 0, 100_000_000],
        # ["starts-with", "$key", f"{remote_dir}/"],
        ["starts-with", "$Content-Type", f"{s3_content_type}"],
        # ['eq', '$x-amz-meta-user-id', userId],
    ]
    # The full filepath for the s3 bucket
    object_name = f"{submission_uuid}/{s3_relative_filepath}"

    presigned_post_url = core.presigned.create_post(
        bucket_name=bucket,
        object_name=object_name,
        conditions=conditions,
        expiration=expiration,
    )
    return presigned_post_url


def create_presigned_get(
    submission_uuid: Union[str, UUID],
    s3_relative_filepath: str,  # Filepath relative to submission dir,
    expiration=3600,
    bucket: str = BUCKET_NAME,
):
    filepath = f"{submission_uuid}/{s3_relative_filepath}"
    logger.debug(f"Creating presigned get for file: {filepath}")
    presigned_get_url = core.presigned.create_get(
        bucket_name=bucket, object_key=filepath, expiration=expiration
    )
    logger.debug(
        f"Returning presigned get for {filepath}: {presigned_get_url}"
    )
    return presigned_get_url
