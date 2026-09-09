from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from app.api.dependencies.auth import (
    get_current_admin,
)
from app.api.dependencies.organization import (
    get_organization_service,
)
from app.models.admin_user import AdminUser
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationResponse,
    OrganizationUpdate,
)
from app.services.organization_service import (
    OrganizationService,
)


router = APIRouter(
    prefix="/organizations",
    tags=["Admin - Organizations"],
)


@router.post(
    "",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_organization(
    payload: OrganizationCreate,
    service: OrganizationService = Depends(
        get_organization_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.create(
        payload
    )


@router.patch(
    "/{organization_id}",
    response_model=OrganizationResponse,
)
def update_organization(
    organization_id: int,
    payload: OrganizationUpdate,
    service: OrganizationService = Depends(
        get_organization_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.update(
        organization_id,
        payload,
    )


@router.delete(
    "/{organization_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_organization(
    organization_id: int,
    service: OrganizationService = Depends(
        get_organization_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    service.delete(
        organization_id
    )

    return Response(
        status_code=(
            status.HTTP_204_NO_CONTENT
        )
    )