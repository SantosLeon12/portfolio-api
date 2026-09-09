from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from app.api.dependencies.auth import (
    get_current_admin,
)
from app.api.dependencies.project import (
    get_project_service,
)
from app.models.admin_user import AdminUser
from app.schemas.project import (
    ProjectCategoryCreate,
    ProjectCategoryResponse,
    ProjectCategoryUpdate,
)
from app.services.project_service import (
    ProjectService,
)


router = APIRouter(
    prefix="/project-categories",
    tags=["Admin - Project Categories"],
)


@router.get(
    "",
    response_model=list[
        ProjectCategoryResponse
    ],
)
def get_categories(
    service: ProjectService = Depends(
        get_project_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.get_categories()


@router.post(
    "",
    response_model=ProjectCategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    payload: ProjectCategoryCreate,
    service: ProjectService = Depends(
        get_project_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.create_category(
        payload
    )


@router.patch(
    "/{category_id}",
    response_model=ProjectCategoryResponse,
)
def update_category(
    category_id: int,
    payload: ProjectCategoryUpdate,
    service: ProjectService = Depends(
        get_project_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.update_category(
        category_id,
        payload,
    )


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_category(
    category_id: int,
    service: ProjectService = Depends(
        get_project_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    service.delete_category(
        category_id
    )

    return Response(status_code=204)