from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from app.api.dependencies.auth import (
    get_current_admin,
)
from app.api.dependencies.profile_technology import (
    get_profile_technology_service,
)
from app.models.admin_user import AdminUser
from app.schemas.technology import (
    ProfileTechnologyCreate,
    ProfileTechnologyListResponse,
    ProfileTechnologyResponse,
    ProfileTechnologyUpdate,
)
from app.services.profile_technology_service import (
    ProfileTechnologyService,
)


router = APIRouter(
    prefix="/profile/technologies",
    tags=["Admin - Profile Technologies"],
)


@router.get(
    "",
    response_model=ProfileTechnologyListResponse,
)
def get_profile_technologies(
    service: ProfileTechnologyService = Depends(
        get_profile_technology_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    items, total = service.get_all()

    return ProfileTechnologyListResponse(
        items=items,
        total=total,
    )


@router.post(
    "",
    response_model=ProfileTechnologyResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_profile_technology(
    payload: ProfileTechnologyCreate,
    service: ProfileTechnologyService = Depends(
        get_profile_technology_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.create(payload)


@router.patch(
    "/{technology_id}",
    response_model=ProfileTechnologyResponse,
)
def update_profile_technology(
    technology_id: int,
    payload: ProfileTechnologyUpdate,
    service: ProfileTechnologyService = Depends(
        get_profile_technology_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.update(
        technology_id,
        payload,
    )


@router.delete(
    "/{technology_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_profile_technology(
    technology_id: int,
    service: ProfileTechnologyService = Depends(
        get_profile_technology_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    service.delete(technology_id)

    return Response(status_code=204)