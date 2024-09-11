from typing import Union
from pathlib import Path
from uuid import UUID

from . import core
from . import buckets

BUCKET_NAME = buckets.JOB
JSON_FILE = "ceonstock_job.json"


# TODO safe to delete this?
# def create(job_uuid: Union[str, UUID], json_data: dict, bucket: str = BUCKET_NAME):
#     json_file_key = f"{job_uuid}/{JSON_FILE}"
#     core.json_s3.save_dict_as_json(bucket, json_data, json_file_key)


def read_json(job_uuid: Union[str, UUID], bucket: str = BUCKET_NAME):
    json_file_key = f"{job_uuid}/{JSON_FILE}"
    json_dict = core.json_s3.read_json_as_dict(bucket, json_file_key)
    return json_dict


def save_json(
    job_uuid: Union[str, UUID], dict_to_save: dict, bucket: str = BUCKET_NAME
):
    """Create the json file or overwrite it if it already exists"""
    json_file_key = f"{job_uuid}/{JSON_FILE}"
    core.json_s3.save_dict_as_json(bucket, dict_to_save, json_file_key)
    return


def save_json_string(
    job_uuid: Union[str, UUID], json_string: str, bucket: str = BUCKET_NAME
):
    """Create the json file or overwrite it if it already exists
    Expects the json data as a json string"""
    json_file_key = f"{job_uuid}/{JSON_FILE}"
    core.json_s3.save_directly_as_json(bucket, json_string, json_file_key)
    return


def list_files(job_uuid: Union[str, UUID], bucket: str = BUCKET_NAME):
    job_dir_key = f"{job_uuid}/"
    found_files = core.inspect.list_s3_files(bucket, job_dir_key)
    return found_files


def list_files_job_inputs(
    job_uuid: Union[str, UUID], bucket: str = BUCKET_NAME
):
    # TODO single source of truth for dir/folder names
    job_dir_key = f"{job_uuid}/job_inputs/"
    found_files = core.inspect.list_s3_files(bucket, job_dir_key)
    return found_files


def list_files_job_outputs(
    job_uuid: Union[str, UUID], bucket: str = BUCKET_NAME
):
    # TODO single source of truth for dir/folder names
    job_dir_key = f"{job_uuid}/job_outputs/"
    found_files = core.inspect.list_s3_files(bucket, job_dir_key)
    return found_files


def download_file(
    job_uuid: Union[str, UUID],
    remote_file_path_relative: str,
    local_dir: str,
    bucket: str = BUCKET_NAME,
) -> Path:
    """
    Download a single file from the s3 job directory.
    remote_file_path_relative: The remote key relative to the job's root dir
    """
    job_root_dir = str(job_uuid)
    remote_file_path = f"{job_root_dir}/{remote_file_path_relative}"
    file_name = Path(remote_file_path).name
    local_file_path = f"{local_dir}/{file_name}"
    result = core.download.file(
        bucket_name=bucket,
        remote_file_path=remote_file_path,
        local_file_path=local_file_path,
    )
    return Path(result)


def upload_file(
    job_uuid: Union[str, UUID],
    local_file_path: str,
    remote_dir_relative: str,
    bucket: str = BUCKET_NAME,
) -> str:
    """
    Upload a single file from the local filesystem into the target remote dir.
    remote_dir_relative: The remote dir relative to the job's root dir
    """
    job_root_dir = str(job_uuid)
    file_name = Path(local_file_path).name
    # Convert to path to handle double backslashes in case remote_dir is empty
    remote_file_path = Path(
        f"{job_root_dir}/{remote_dir_relative}/{file_name}"
    )
    result = core.upload.file(
        bucket_name=bucket,
        local_file=local_file_path,
        remote_file=str(remote_file_path),
    )
    return str(result)


def upload_job_input(
    job_uuid: Union[str, UUID],
    local_file_path: str,
    bucket: str = BUCKET_NAME,
) -> str:
    """
    Upload a single file from the local filesystem into the remote job_inputs dir.
    """
    job_root_dir = str(job_uuid)
    file_name = Path(local_file_path).name
    # Convert to path to handle double backslashes in case remote_dir is empty
    remote_file_path = Path(f"{job_root_dir}/job_inputs/{file_name}")
    result = core.upload.file(
        bucket_name=bucket,
        local_file=str(local_file_path),
        remote_file=str(remote_file_path),
    )
    return str(result)
