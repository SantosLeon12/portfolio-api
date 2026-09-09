from fastapi import APIRouter, Depends

from app.api.dependencies.language import (
    get_language_service,
)
from app.schemas.language import (
    ProfileLanguageListResponse,
)
from app.services.language_service import (
    LanguageService,
)


router = APIRouter(
    prefix="/languages",
    tags=["Public - Languages"],
)


@router.get(
    "",
    response_model=ProfileLanguageListResponse,
)
def get_languages(
    service: LanguageService = Depends(
        get_language_service
    ),
):
    items, total = (
        service.get_profile_languages()
    )

    return ProfileLanguageListResponse(
        items=items,
        total=total,
    )