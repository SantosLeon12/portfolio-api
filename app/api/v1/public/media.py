from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import Session

from app.database.dependencies import (
    get_db,
)
from app.repositories.public_media_repository import (
    PublicMediaRepository,
)
from app.schemas.public_media import (
    PublicProfileDocumentResponse,
    PublicProfileMediaResponse,
    PublicProjectMediaResponse,
)
from app.services.public_media_service import (
    PublicMediaService,
)


router = APIRouter(
    prefix="/media",
    tags=[
        "Public - Media",
    ],
)


def get_public_media_service(
    db: Session = Depends(
        get_db
    ),
):
    repository = (
        PublicMediaRepository(
            db
        )
    )

    return PublicMediaService(
        repository
    )


# =========================================================
# PROFILE MEDIA
# =========================================================

@router.get(
    "/profile",
    response_model=list[
        PublicProfileMediaResponse
    ],
)
def get_profile_media(
    service:
        PublicMediaService
        = Depends(
            get_public_media_service
        ),
):
    return (
        service
        .get_profile_media()
    )


# =========================================================
# PROFILE DOCUMENTS
# =========================================================

@router.get(
    "/documents",
    response_model=list[
        PublicProfileDocumentResponse
    ],
)
def get_profile_documents(
    service:
        PublicMediaService
        = Depends(
            get_public_media_service
        ),
):
    return (
        service
        .get_profile_documents()
    )


# =========================================================
# PROJECT MEDIA
# =========================================================

@router.get(
    "/projects/{project_slug}",
    response_model=list[
        PublicProjectMediaResponse
    ],
)
def get_project_media(
    project_slug: str,
    service:
        PublicMediaService
        = Depends(
            get_public_media_service
        ),
):
    return (
        service
        .get_project_media(
            project_slug
        )
    )