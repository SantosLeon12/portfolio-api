from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class MediaAssetResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    storage_provider: str
    storage_key: str
    url: str

    mime_type: str | None
    file_size: int | None

    width: int | None
    height: int | None

    created_at: datetime


class MediaAssetListResponse(BaseModel):
    items: list[MediaAssetResponse]
    total: int


# =========================================================
# PROFILE MEDIA
# =========================================================

class ProfileMediaCreate(BaseModel):
    media_asset_id: int

    media_role: str = Field(
        min_length=1,
        max_length=30,
    )

    alt_text: str | None = Field(
        default=None,
        max_length=255,
    )

    display_order: int = Field(
        default=0,
        ge=0,
    )


class ProfileMediaUpdate(BaseModel):
    media_role: str | None = Field(
        default=None,
        min_length=1,
        max_length=30,
    )

    alt_text: str | None = Field(
        default=None,
        max_length=255,
    )

    display_order: int | None = Field(
        default=None,
        ge=0,
    )


class ProfileMediaResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    media_role: str
    alt_text: str | None
    display_order: int

    media_asset: MediaAssetResponse

class ProfileMediaListResponse(
    BaseModel
):
    items: list[
        ProfileMediaResponse
    ]

    total: int

# =========================================================
# PROFILE DOCUMENT
# =========================================================

class ProfileDocumentCreate(BaseModel):
    media_asset_id: int

    document_type: str = Field(
        min_length=1,
        max_length=30,
    )

    title: str = Field(
        min_length=1,
        max_length=180,
    )

    version: str | None = Field(
        default=None,
        max_length=50,
    )

    is_current: bool = False


class ProfileDocumentUpdate(BaseModel):
    document_type: str | None = Field(
        default=None,
        min_length=1,
        max_length=30,
    )

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=180,
    )

    version: str | None = Field(
        default=None,
        max_length=50,
    )

    is_current: bool | None = None


class ProfileDocumentResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    document_type: str
    title: str
    version: str | None
    is_current: bool

    media_asset: MediaAssetResponse

    created_at: datetime
    updated_at: datetime

class ProfileDocumentListResponse(
    BaseModel
):
    items: list[
        ProfileDocumentResponse
    ]

    total: int