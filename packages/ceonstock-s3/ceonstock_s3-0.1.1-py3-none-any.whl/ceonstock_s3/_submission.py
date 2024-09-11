import uuid
import logging
from typing import List
from pathlib import Path

from .log import printify
from . import s3_manager
from . import errors

logger = logging.getLogger(__name__)
# logger.setLevel("DEBUG")

BUCKET_NAME = "ceonstock-submission-bucket"


async def create_presigned_upload_url(
    remote_key: str,
    content_type: str,
    bucket=BUCKET_NAME,
):
    # S3_CONTENT_TYPES = {
    #     CstockProjInput.web_input_types.DOC: "application/",
    #     CstockProjInput.web_input_types.IMG: "image/",
    # }

    S3_CONTENT_TYPES = {
        "doc": "application/",
        "image": "image/",
    }
    content_type = S3_CONTENT_TYPES[content_type]
    logger.debug(f"Got content_type: {content_type}")
    # TODO stricter content-type checking (record content-type when uploaded)
    conditions = [
        ["content-length-range", 0, 100_000_000],
        # ["starts-with", "$key", f"{remote_dir}/"],
        ["starts-with", "$Content-Type", f"{content_type}"],
        # ['eq', '$x-amz-meta-user-id', userId],
    ]
    logger.debug(
        f"Creating presigned url: {printify({'bucket': bucket, 'remote_key': remote_key, 'conditions': conditions})}"
    )
    try:
        presigned_url = s3_manager.create_presigned_post(
            bucket, remote_key, conditions=conditions
        )
        logger.debug("Created presigned url: presigned_url")
        return presigned_url
    except Exception as e:
        logger.error(f"Failed to get presigned upload url: {e}")
        raise e


class Submission:
    def __init__(self, submission_uuid: uuid.UUID):
        self.uuid = submission_uuid

    async def create_presigned_upload_urls(
        self, *, user_inputs, proj_inputs: List[CstockProjInput]
    ):
        # input_forms_with_files = InputsHandler.filter_for_file_inputs(
        # submission_inputs, proj_inputs
        # )
        logger.debug(f"Got submission_uuid: {self.uuid}")
        logger.debug(f"Got proj_inputs: {proj_inputs}")
        logger.debug(f"Got user_inputs: {user_inputs}")
        keyed_user_inputs = {user_input.name: user_input for user_input in user_inputs}
        remote_dir = Path(str(self.uuid))
        form_upload_urls = {}
        for proj_input in proj_inputs:
            if not proj_input.type().info().is_file:
                logger.debug(
                    f"proj_input({proj_input.name}) is not a file type. Skipping generation of presigned upload url."
                )
                continue  # No upload required for non-file submissions
            file_upload_urls = []
            user_input = keyed_user_inputs[proj_input.name]
            if len(user_input.entries) > 5:
                # TODO more elegant per-project limit management
                raise errors.S3UploadError(
                    message="Cannot submit more than 5 files for a single input",
                )
            for entry in user_input.entries:
                logger.debug(f"Got entry: {entry}")
                file_name = Path(entry.value).name
                logger.info(f"file_name: {file_name}")
                remote_key = f"{remote_dir}/{file_name}"
                presigned_url = await create_presigned_upload_url(
                    remote_key, proj_input
                )
                file_upload_urls.append(presigned_url)

            form_upload_urls[proj_input.name] = file_upload_urls
        logger.debug(f"Create form_upload_urls: {form_upload_urls}")
        return form_upload_urls
