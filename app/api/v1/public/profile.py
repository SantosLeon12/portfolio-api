from fastapi import (
    APIRouter,
    Depends,
)

from app.api.dependencies.profile import (
    get_profile_service,
)
from app.schemas.profile import (
    ProfileResponse,
)
from app.services.profile_service import (
    ProfileService,
)


router = APIRouter(
    prefix="/profile",
    tags=["Public - Profile"],
)


@router.get(
    "",
    response_model=ProfileResponse,
)
def get_profile(
    service: ProfileService = Depends(
        get_profile_service
    ),
):
    return service.get_profile(
        public_only=True
    )