from typing import BinaryIO

import cloudinary
import cloudinary.uploader

from app.core.config import settings


cloudinary.config(
    cloud_name=settings.cloudinary_cloud_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
    secure=True,
)


def get_resource_type(
    mime_type: str,
) -> str:
    if mime_type.startswith("image/"):
        return "image"

    if mime_type == "application/pdf":
        return "image"

    return "raw"


def upload_to_cloudinary(
    file: BinaryIO,
    mime_type: str,
    folder: str = "portfolio",
) -> dict:
    resource_type = get_resource_type(
        mime_type
    )

    return cloudinary.uploader.upload(
        file,
        folder=folder,
        resource_type=resource_type,
        use_filename=True,
        unique_filename=True,
        overwrite=False,
    )


def delete_from_cloudinary(
    storage_key: str,
    mime_type: str,
) -> None:
    resource_type = get_resource_type(
        mime_type
    )

    cloudinary.uploader.destroy(
        storage_key,
        resource_type=resource_type,
        invalidate=True,
    )