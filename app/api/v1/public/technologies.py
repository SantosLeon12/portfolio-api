from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.technology import (
    TechnologyCategoryResponse,
    TechnologyListResponse,
    TechnologyResponse,
)
from app.services.technology_service import TechnologyService

from app.api.dependencies.technology import (
    get_technology_service,
)

router = APIRouter(
    prefix="/technologies",
    tags=["Public - Technologies"],
)


@router.get(
    "",
    response_model=TechnologyListResponse,
)
def get_technologies(
    service: TechnologyService = Depends(
        get_technology_service
    ),
):
    technologies, total = service.get_all()

    return TechnologyListResponse(
        items=technologies,
        total=total,
    )


@router.get(
    "/categories",
    response_model=list[TechnologyCategoryResponse],
)
def get_technology_categories(
    service: TechnologyService = Depends(
        get_technology_service
    ),
):
    return service.get_categories()


@router.get(
    "/{slug}",
    response_model=TechnologyResponse,
)
def get_technology_by_slug(
    slug: str,
    service: TechnologyService = Depends(
        get_technology_service
    ),
):
    technology = service.get_by_slug(
        slug=slug,
    )

    if technology is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Technology not found",
        )

    return technology