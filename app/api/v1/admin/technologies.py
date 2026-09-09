from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from app.api.dependencies.auth import (
    get_current_admin,
)
from app.api.dependencies.technology import (
    get_technology_service,
)
from app.models.admin_user import AdminUser
from app.schemas.technology import (
    TechnologyCreate,
    TechnologyResponse,
    TechnologyUpdate,
)
from app.services.technology_service import (
    TechnologyService,
)


router = APIRouter(
    prefix="/technologies",
    tags=["Admin - Technologies"],
)


@router.post(
    "",
    response_model=TechnologyResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_technology(
    payload: TechnologyCreate,
    service: TechnologyService = Depends(
        get_technology_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.create_technology(
        payload
    )


@router.patch(
    "/{technology_id}",
    response_model=TechnologyResponse,
)
def update_technology(
    technology_id: int,
    payload: TechnologyUpdate,
    service: TechnologyService = Depends(
        get_technology_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.update_technology(
        technology_id=technology_id,
        data=payload,
    )


@router.delete(
    "/{technology_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_technology(
    technology_id: int,
    service: TechnologyService = Depends(
        get_technology_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    service.delete_technology(
        technology_id
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )