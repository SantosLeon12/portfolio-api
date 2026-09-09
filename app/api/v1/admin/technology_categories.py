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
    TechnologyCategoryCreate,
    TechnologyCategoryResponse,
    TechnologyCategoryUpdate,
)
from app.services.technology_service import (
    TechnologyService,
)


router = APIRouter(
    prefix="/technology-categories",
    tags=["Admin - Technology Categories"],
)


@router.post(
    "",
    response_model=TechnologyCategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    payload: TechnologyCategoryCreate,
    service: TechnologyService = Depends(
        get_technology_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.create_category(
        payload
    )


@router.patch(
    "/{category_id}",
    response_model=TechnologyCategoryResponse,
)
def update_category(
    category_id: int,
    payload: TechnologyCategoryUpdate,
    service: TechnologyService = Depends(
        get_technology_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.update_category(
        category_id=category_id,
        data=payload,
    )


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_category(
    category_id: int,
    service: TechnologyService = Depends(
        get_technology_service
    ),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    service.delete_category(
        category_id
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )