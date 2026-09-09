from pydantic import (
    BaseModel,
    ConfigDict,
)


class PublicMediaAssetResponse(
    BaseModel
):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    url: str

    mime_type: str | None

    width: int | None
    height: int | None


class PublicProfileMediaResponse(
    BaseModel
):
    id: int

    media_role: str

    alt_text: str | None

    display_order: int

    media_asset: (
        PublicMediaAssetResponse
    )


class PublicProjectMediaResponse(
    BaseModel
):
    id: int

    media_role: str

    alt_text: str | None

    caption: str | None

    display_order: int

    media_asset: (
        PublicMediaAssetResponse
    )


class PublicProfileDocumentResponse(
    BaseModel
):
    id: int

    document_type: str

    title: str

    version: str | None

    media_asset: (
        PublicMediaAssetResponse
    )