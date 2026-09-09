from fastapi import (
    APIRouter,
    Depends,
)

from app.api.dependencies.profile_technology import (
    get_profile_technology_service,
)
from app.schemas.technology import (
    ProfileTechnologyListResponse,
)
from app.services.profile_technology_service import (
    ProfileTechnologyService,
)


router = APIRouter(
    prefix="/profile/technologies",
    tags=["Public - Profile Technologies"],
)


@router.get(
    "",
    response_model=ProfileTechnologyListResponse,
)
def get_profile_technologies(
    service: ProfileTechnologyService = Depends(
        get_profile_technology_service
    ),
):
    items, total = service.get_all(
        public_only=True
    )

    return ProfileTechnologyListResponse(
        items=items,
        total=total,
    )