from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from app.api.dependencies.auth import (
    get_current_admin,
)
from app.api.dependencies.profile import (
    get_profile_service,
)
from app.models.admin_user import AdminUser
from app.schemas.profile import (
    InterestCreate,
    InterestResponse,
    InterestUpdate,
    ProfileContactCreate,
    ProfileContactResponse,
    ProfileContactUpdate,
    ProfileCreate,
    ProfileResponse,
    ProfileUpdate,
    SocialLinkCreate,
    SocialLinkResponse,
    SocialLinkUpdate,
    StrengthCreate,
    StrengthResponse,
    StrengthUpdate,
)
from app.services.profile_service import (
    ProfileService,
)


router = APIRouter(
    prefix="/profile",
    tags=["Admin - Profile"],
)


# =========================================================
# PROFILE
# =========================================================

@router.post(
    "",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_profile(
    payload: ProfileCreate,
    service: ProfileService = Depends(
        get_profile_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.create_profile(
        payload
    )


@router.patch(
    "",
    response_model=ProfileResponse,
)
def update_profile(
    payload: ProfileUpdate,
    service: ProfileService = Depends(
        get_profile_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.update_profile(
        payload
    )

@router.get(
    "",
    response_model=ProfileResponse,
)
def get_profile(
    service: ProfileService = Depends(
        get_profile_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.get_profile()


# =========================================================
# CONTACTS
# =========================================================

@router.post(
    "/contacts",
    response_model=ProfileContactResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_contact(
    payload: ProfileContactCreate,
    service: ProfileService = Depends(
        get_profile_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.create_contact(
        payload
    )


@router.patch(
    "/contacts/{contact_id}",
    response_model=ProfileContactResponse,
)
def update_contact(
    contact_id: int,
    payload: ProfileContactUpdate,
    service: ProfileService = Depends(
        get_profile_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.update_contact(
        contact_id,
        payload,
    )


@router.delete(
    "/contacts/{contact_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_contact(
    contact_id: int,
    service: ProfileService = Depends(
        get_profile_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    service.delete_contact(
        contact_id
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )


# =========================================================
# SOCIAL LINKS
# =========================================================

@router.post(
    "/social-links",
    response_model=SocialLinkResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_social_link(
    payload: SocialLinkCreate,
    service: ProfileService = Depends(
        get_profile_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.create_social_link(
        payload
    )


@router.patch(
    "/social-links/{social_link_id}",
    response_model=SocialLinkResponse,
)
def update_social_link(
    social_link_id: int,
    payload: SocialLinkUpdate,
    service: ProfileService = Depends(
        get_profile_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.update_social_link(
        social_link_id,
        payload,
    )


@router.delete(
    "/social-links/{social_link_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_social_link(
    social_link_id: int,
    service: ProfileService = Depends(
        get_profile_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    service.delete_social_link(
        social_link_id
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )


# =========================================================
# STRENGTHS
# =========================================================

@router.post(
    "/strengths",
    response_model=StrengthResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_strength(
    payload: StrengthCreate,
    service: ProfileService = Depends(
        get_profile_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.create_strength(
        payload
    )


@router.patch(
    "/strengths/{strength_id}",
    response_model=StrengthResponse,
)
def update_strength(
    strength_id: int,
    payload: StrengthUpdate,
    service: ProfileService = Depends(
        get_profile_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.update_strength(
        strength_id,
        payload,
    )


@router.delete(
    "/strengths/{strength_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_strength(
    strength_id: int,
    service: ProfileService = Depends(
        get_profile_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    service.delete_strength(
        strength_id
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )


# =========================================================
# INTERESTS
# =========================================================

@router.post(
    "/interests",
    response_model=InterestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_interest(
    payload: InterestCreate,
    service: ProfileService = Depends(
        get_profile_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.create_interest(
        payload
    )


@router.patch(
    "/interests/{interest_id}",
    response_model=InterestResponse,
)
def update_interest(
    interest_id: int,
    payload: InterestUpdate,
    service: ProfileService = Depends(
        get_profile_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.update_interest(
        interest_id,
        payload,
    )


@router.delete(
    "/interests/{interest_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_interest(
    interest_id: int,
    service: ProfileService = Depends(
        get_profile_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    service.delete_interest(
        interest_id
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )