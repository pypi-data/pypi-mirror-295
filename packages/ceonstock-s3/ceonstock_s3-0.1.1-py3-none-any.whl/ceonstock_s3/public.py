import logging
from pathlib import Path
from typing import Union
from uuid import UUID

from . import core
from . import buckets

BUCKET_NAME = buckets.PUBLIC
EXAMPLE_VIDEO_SUFFIX = ".webm"
EXAMPLE_THUMBNAIL_SUFFIX = ".jpg"

logger = logging.getLogger(__name__)


def upload_project_example_video(
    local_file: Union[str, Path],
    project_uuid: Union[str, UUID],
    bucket: str = BUCKET_NAME,
) -> str:
    filename = Path(local_file).with_stem("video").name
    if Path(local_file).suffix != EXAMPLE_VIDEO_SUFFIX:
        logger.warning(
            f"Uploaded file {filename} does not contain expected file extension {EXAMPLE_VIDEO_SUFFIX}"
        )
    remote_file = f"projects/{project_uuid}/{filename}"
    result = core.upload.file(BUCKET_NAME, local_file, remote_file)
    logger.debug(f"Got s3 core upload result: {result}")
    return remote_file


def upload_project_thumbnail(
    local_file: Union[str, Path],
    project_uuid: Union[str, UUID],
    bucket: str = BUCKET_NAME,
) -> str:
    filename = Path(local_file).with_stem("thumbnail").name
    if Path(local_file).suffix != EXAMPLE_THUMBNAIL_SUFFIX:
        logger.warning(
            f"Uploaded file {filename} does not contain expected file extension {EXAMPLE_THUMBNAIL_SUFFIX}"
        )
    remote_file = f"projects/{project_uuid}/{filename}"
    result = core.upload.file(BUCKET_NAME, local_file, remote_file)
    logger.debug(f"Got s3 core upload result: {result}")
    return remote_file


def upload_project_input_example_vtt(
    local_file: Union[str, Path],
    project_uuid: Union[str, UUID],
    project_input_name: str,
    bucket: str = BUCKET_NAME,
) -> str:
    # Force rename the file to match the project input name
    filename = Path(local_file).with_stem(project_input_name).name
    if Path(local_file).suffix != ".vtt":
        raise Exception(
            f"local file {local_file} does not contain required suffix: .vtt"
        )
    remote_file = (
        f"projects/{project_uuid}/examples/{project_input_name}/{filename}"
    )
    result = core.upload.file(BUCKET_NAME, local_file, remote_file)
    logger.debug(f"Got s3 core upload result: {result}")
    return remote_file


def upload_project_input_example_video(
    local_file: Union[str, Path],
    project_uuid: Union[str, UUID],
    project_input_name: str,
    bucket: str = BUCKET_NAME,
) -> str:
    # Force rename the file to match the project input name
    filename = Path(local_file).with_stem(project_input_name).name
    if Path(local_file).suffix != EXAMPLE_VIDEO_SUFFIX:
        logger.warning(
            f"Uploaded file {filename} does not contain expected file extension {EXAMPLE_VIDEO_SUFFIX}"
        )
    remote_file = (
        f"projects/{project_uuid}/examples/{project_input_name}/{filename}"
    )
    result = core.upload.file(BUCKET_NAME, local_file, remote_file)
    logger.debug(f"Got s3 core upload result: {result}")
    return remote_file


def upload_project_input_example_input_file(
    local_file: Union[str, Path],
    project_uuid: Union[str, UUID],
    project_input_name: str,
    bucket: str = BUCKET_NAME,
) -> str:
    # Force rename the file to match the project input name
    filename = Path(local_file).name
    if Path(local_file).suffix != EXAMPLE_VIDEO_SUFFIX:
        logger.warning(
            f"Uploaded file {filename} does not contain expected file extension {EXAMPLE_VIDEO_SUFFIX}"
        )
    remote_file = f"projects/{project_uuid}/examples/{project_input_name}/input_files/{filename}"
    result = core.upload.file(BUCKET_NAME, local_file, remote_file)
    logger.debug(f"Got s3 core upload result: {result}")
    return remote_file


# def download(
#     project_uuid: Union[str, UUID], local_dir: str, bucket: str = BUCKET_NAME
# ):
#     # TODO test this (this function was created when it wasn't needed and may not have been tested).
#     remote_file = f"{project_uuid}.zip"
#     download_as_file = f"{local_dir}/{project_uuid}.zip"
#     result = core.download.file(BUCKET_NAME, remote_file, download_as_file)
#     return result
