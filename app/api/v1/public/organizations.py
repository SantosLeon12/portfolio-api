from fastapi import (
    APIRouter,
    Depends,
)

from app.api.dependencies.organization import (
    get_organization_service,
)
from app.schemas.organization import (
    OrganizationListResponse,
    OrganizationResponse,
)
from app.services.organization_service import (
    OrganizationService,
)


router = APIRouter(
    prefix="/organizations",
    tags=["Public - Organizations"],
)


@router.get(
    "",
    response_model=OrganizationListResponse,
)
def get_organizations(
    service: OrganizationService = Depends(
        get_organization_service
    ),
):
    organizations, total = (
        service.get_all()
    )

    return OrganizationListResponse(
        items=organizations,
        total=total,
    )


@router.get(
    "/{organization_id}",
    response_model=OrganizationResponse,
)
def get_organization(
    organization_id: int,
    service: OrganizationService = Depends(
        get_organization_service
    ),
):
    return service.get_by_id(
        organization_id
    )