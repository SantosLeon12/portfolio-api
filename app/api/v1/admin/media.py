from fastapi import (
    APIRouter,
    Depends,
    File,
    Response,
    UploadFile,
    status,
)

from app.api.dependencies.auth import (
    get_current_admin,
)
from app.api.dependencies.media import (
    get_media_service,
)
from app.models.admin_user import AdminUser
from app.schemas.media import (
    MediaAssetListResponse,
    MediaAssetResponse,
    ProfileDocumentCreate,
    ProfileDocumentResponse,
    ProfileDocumentUpdate,
    ProfileMediaCreate,
    ProfileMediaResponse,
    ProfileMediaUpdate,
    ProfileDocumentListResponse,
    ProfileMediaListResponse,
)
from app.services.media_service import (
    MediaService,
)


router = APIRouter(
    tags=["Admin - Media"],
)


@router.get(
    "/media",
    response_model=MediaAssetListResponse,
)
def get_media_assets(
    service: MediaService = Depends(
        get_media_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    items, total = service.get_all()

    return MediaAssetListResponse(
        items=items,
        total=total,
    )


@router.get(
    "/media/{media_asset_id}",
    response_model=MediaAssetResponse,
)
def get_media_asset(
    media_asset_id: int,
    service: MediaService = Depends(
        get_media_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.get_asset(
        media_asset_id
    )


@router.post(
    "/media/upload",
    response_model=MediaAssetResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_media(
    file: UploadFile = File(...),
    service: MediaService = Depends(
        get_media_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.upload(file)


@router.delete(
    "/media/{media_asset_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_media(
    media_asset_id: int,
    service: MediaService = Depends(
        get_media_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    service.delete_asset(
        media_asset_id
    )

    return Response(
        status_code=204
    )

@router.get(
    "/profile/media",
    response_model=ProfileMediaListResponse,
)
def get_profile_media(
    service: MediaService = Depends(
        get_media_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    items = (
        service
        .get_profile_media_items()
    )

    return ProfileMediaListResponse(
        items=items,
        total=len(items),
    )

# PROFILE MEDIA

@router.post(
    "/profile/media",
    response_model=ProfileMediaResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_profile_media(
    payload: ProfileMediaCreate,
    service: MediaService = Depends(
        get_media_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.create_profile_media(
        payload
    )


@router.patch(
    "/profile/media/{profile_media_id}",
    response_model=ProfileMediaResponse,
)
def update_profile_media(
    profile_media_id: int,
    payload: ProfileMediaUpdate,
    service: MediaService = Depends(
        get_media_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.update_profile_media(
        profile_media_id,
        payload,
    )


@router.delete(
    "/profile/media/{profile_media_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_profile_media(
    profile_media_id: int,
    service: MediaService = Depends(
        get_media_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    service.delete_profile_media(
        profile_media_id
    )

    return Response(status_code=204)


# PROFILE DOCUMENTS

@router.get(
    "/profile/documents",
    response_model=ProfileDocumentListResponse,
)
def get_profile_documents(
    service: MediaService = Depends(
        get_media_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    items = (
        service.get_documents()
    )

    return ProfileDocumentListResponse(
        items=items,
        total=len(items),
    )

@router.post(
    "/profile/documents",
    response_model=ProfileDocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_document(
    payload: ProfileDocumentCreate,
    service: MediaService = Depends(
        get_media_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.create_document(
        payload
    )


@router.patch(
    "/profile/documents/{document_id}",
    response_model=ProfileDocumentResponse,
)
def update_document(
    document_id: int,
    payload: ProfileDocumentUpdate,
    service: MediaService = Depends(
        get_media_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.update_document(
        document_id,
        payload,
    )


@router.delete(
    "/profile/documents/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_document(
    document_id: int,
    service: MediaService = Depends(
        get_media_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    service.delete_document(
        document_id
    )

    return Response(status_code=204)