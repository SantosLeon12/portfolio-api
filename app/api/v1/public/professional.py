from fastapi import (
    APIRouter,
    Depends,
)

from app.api.dependencies.professional import (
    get_professional_service,
)
from app.schemas.professional import (
    EducationListResponse,
    ExperienceListResponse,
)
from app.services.professional_service import (
    ProfessionalService,
)


router = APIRouter(
    tags=["Public - Professional"],
)


@router.get(
    "/experiences",
    response_model=ExperienceListResponse,
)
def get_experiences(
    service: ProfessionalService = Depends(
        get_professional_service
    ),
):
    items, total = service.get_experiences(
        public_only=True
    )

    return ExperienceListResponse(
        items=items,
        total=total,
    )


@router.get(
    "/educations",
    response_model=EducationListResponse,
)
def get_educations(
    service: ProfessionalService = Depends(
        get_professional_service
    ),
):
    items, total = service.get_educations(
        public_only=True
    )

    return EducationListResponse(
        items=items,
        total=total,
    )