from fastapi import (
    APIRouter,
    Depends,
)

from app.api.dependencies.project import (
    get_project_service,
)
from app.schemas.project import (
    ProjectListResponse,
    ProjectResponse,
)
from app.services.project_service import (
    ProjectService,
)


router = APIRouter(
    prefix="/projects",
    tags=["Public - Projects"],
)


@router.get(
    "",
    response_model=ProjectListResponse,
)
def get_projects(
    featured: bool | None = None,
    service: ProjectService = Depends(
        get_project_service
    ),
):
    items, total = service.get_projects(
        public_only=True,
        featured=featured,
    )

    return ProjectListResponse(
        items=items,
        total=total,
    )


@router.get(
    "/{slug}",
    response_model=ProjectResponse,
)
def get_project(
    slug: str,
    service: ProjectService = Depends(
        get_project_service
    ),
):
    return service.get_public_by_slug(
        slug
    )