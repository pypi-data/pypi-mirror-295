from typing import Union
from uuid import UUID

from . import core
from . import buckets

BUCKET_NAME = buckets.PROJECT


def upload(project_uuid: Union[str, UUID], local_file: str, bucket: str = BUCKET_NAME):
    remote_file = f"{project_uuid}.zip"
    result = core.upload.file(BUCKET_NAME, local_file, remote_file)
    return result


def download(project_uuid: Union[str, UUID], local_dir: str, bucket: str = BUCKET_NAME):
    # TODO test this (this function was created when it wasn't needed and may not have been tested).
    remote_file = f"{project_uuid}.zip"
    download_as_file = f"{local_dir}/{project_uuid}.zip"
    result = core.download.file(BUCKET_NAME, remote_file, download_as_file)
    return result
