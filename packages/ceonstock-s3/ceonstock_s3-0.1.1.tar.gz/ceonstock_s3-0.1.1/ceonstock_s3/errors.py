from dataclasses import dataclass


# Base exception
class S3Error(Exception):
    ...


@dataclass
class S3FileNotFoundError(S3Error):
    bucket: str
    key: str


@dataclass
class S3UploadError(S3Error):
    message: str


@dataclass
class S3ReadError(S3Error):
    message: str
