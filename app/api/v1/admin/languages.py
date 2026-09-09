from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from app.api.dependencies.auth import (
    get_current_admin,
)
from app.api.dependencies.language import (
    get_language_service,
)
from app.models.admin_user import AdminUser
from app.schemas.language import (
    LanguageCreate,
    LanguageResponse,
    LanguageUpdate,
    ProfileLanguageCreate,
    ProfileLanguageListResponse,
    ProfileLanguageResponse,
    ProfileLanguageUpdate,
    ProficiencyLevelCreate,
    ProficiencyLevelResponse,
    ProficiencyLevelUpdate,
)
from app.services.language_service import (
    LanguageService,
)


router = APIRouter(
    prefix="/languages",
    tags=["Admin - Languages"],
)


# =========================================================
# LANGUAGES
# =========================================================

@router.get(
    "",
    response_model=list[LanguageResponse],
)
def get_languages(
    service: LanguageService = Depends(
        get_language_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.get_languages()


@router.post(
    "",
    response_model=LanguageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_language(
    payload: LanguageCreate,
    service: LanguageService = Depends(
        get_language_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.create_language(
        payload
    )


@router.patch(
    "/{language_id}",
    response_model=LanguageResponse,
)
def update_language(
    language_id: int,
    payload: LanguageUpdate,
    service: LanguageService = Depends(
        get_language_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.update_language(
        language_id,
        payload,
    )


@router.delete(
    "/{language_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_language(
    language_id: int,
    service: LanguageService = Depends(
        get_language_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    service.delete_language(
        language_id
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )


# =========================================================
# PROFICIENCY LEVELS
# =========================================================

@router.get(
    "/proficiency-levels",
    response_model=list[ProficiencyLevelResponse],
)
def get_proficiency_levels(
    service: LanguageService = Depends(
        get_language_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.get_levels()


@router.post(
    "/proficiency-levels",
    response_model=ProficiencyLevelResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_proficiency_level(
    payload: ProficiencyLevelCreate,
    service: LanguageService = Depends(
        get_language_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.create_level(
        payload
    )


@router.patch(
    "/proficiency-levels/{level_id}",
    response_model=ProficiencyLevelResponse,
)
def update_proficiency_level(
    level_id: int,
    payload: ProficiencyLevelUpdate,
    service: LanguageService = Depends(
        get_language_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.update_level(
        level_id,
        payload,
    )


@router.delete(
    "/proficiency-levels/{level_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_proficiency_level(
    level_id: int,
    service: LanguageService = Depends(
        get_language_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    service.delete_level(
        level_id
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )


# =========================================================
# PROFILE LANGUAGES
# =========================================================

@router.get(
    "/profile",
    response_model=ProfileLanguageListResponse,
)
def get_profile_languages(
    service: LanguageService = Depends(
        get_language_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    items, total = (
        service.get_profile_languages()
    )

    return ProfileLanguageListResponse(
        items=items,
        total=total,
    )


@router.post(
    "/profile",
    response_model=ProfileLanguageResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_profile_language(
    payload: ProfileLanguageCreate,
    service: LanguageService = Depends(
        get_language_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.add_profile_language(
        payload
    )


@router.patch(
    "/profile/{language_id}",
    response_model=ProfileLanguageResponse,
)
def update_profile_language(
    language_id: int,
    payload: ProfileLanguageUpdate,
    service: LanguageService = Depends(
        get_language_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.update_profile_language(
        language_id,
        payload,
    )


@router.delete(
    "/profile/{language_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_profile_language(
    language_id: int,
    service: LanguageService = Depends(
        get_language_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    service.delete_profile_language(
        language_id
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )