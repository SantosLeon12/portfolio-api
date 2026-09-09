from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from app.api.dependencies.auth import (
    get_current_admin,
)
from app.api.dependencies.professional import (
    get_professional_service,
)
from app.models.admin_user import AdminUser
from app.schemas.professional import (
    EducationCreate,
    EducationListResponse,
    EducationResponse,
    EducationUpdate,
    ExperienceCreate,
    ExperienceHighlightCreate,
    ExperienceHighlightResponse,
    ExperienceHighlightUpdate,
    ExperienceListResponse,
    ExperienceResponse,
    ExperienceTechnologyCreate,
    ExperienceTechnologyResponse,
    ExperienceTechnologyUpdate,
    ExperienceUpdate,
)
from app.services.professional_service import (
    ProfessionalService,
)


router = APIRouter(
    tags=["Admin - Professional"],
)


# EXPERIENCE

@router.get(
    "/experiences",
    response_model=ExperienceListResponse,
)
def get_experiences(
    service: ProfessionalService = Depends(
        get_professional_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    items, total = service.get_experiences()

    return ExperienceListResponse(
        items=items,
        total=total,
    )

@router.get(
    "/experiences/{experience_id}",
    response_model=ExperienceResponse,
)
def get_experience(
    experience_id: int,
    service: ProfessionalService = Depends(
        get_professional_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.get_experience(
        experience_id
    )


@router.post(
    "/experiences",
    response_model=ExperienceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_experience(
    payload: ExperienceCreate,
    service: ProfessionalService = Depends(
        get_professional_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.create_experience(
        payload
    )


@router.patch(
    "/experiences/{experience_id}",
    response_model=ExperienceResponse,
)
def update_experience(
    experience_id: int,
    payload: ExperienceUpdate,
    service: ProfessionalService = Depends(
        get_professional_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.update_experience(
        experience_id,
        payload,
    )


@router.delete(
    "/experiences/{experience_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_experience(
    experience_id: int,
    service: ProfessionalService = Depends(
        get_professional_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    service.delete_experience(
        experience_id
    )

    return Response(
        status_code=204
    )


# HIGHLIGHTS

@router.post(
    "/experiences/{experience_id}/highlights",
    response_model=ExperienceHighlightResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_highlight(
    experience_id: int,
    payload: ExperienceHighlightCreate,
    service: ProfessionalService = Depends(
        get_professional_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.create_highlight(
        experience_id,
        payload,
    )


@router.patch(
    "/experiences/{experience_id}/highlights/{highlight_id}",
    response_model=ExperienceHighlightResponse,
)
def update_highlight(
    experience_id: int,
    highlight_id: int,
    payload: ExperienceHighlightUpdate,
    service: ProfessionalService = Depends(
        get_professional_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.update_highlight(
        experience_id,
        highlight_id,
        payload,
    )


@router.delete(
    "/experiences/{experience_id}/highlights/{highlight_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_highlight(
    experience_id: int,
    highlight_id: int,
    service: ProfessionalService = Depends(
        get_professional_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    service.delete_highlight(
        experience_id,
        highlight_id,
    )

    return Response(
        status_code=204
    )


# EXPERIENCE TECHNOLOGIES

@router.post(
    "/experiences/{experience_id}/technologies",
    response_model=ExperienceTechnologyResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_experience_technology(
    experience_id: int,
    payload: ExperienceTechnologyCreate,
    service: ProfessionalService = Depends(
        get_professional_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.add_technology(
        experience_id,
        payload,
    )


@router.patch(
    "/experiences/{experience_id}/technologies/{technology_id}",
    response_model=ExperienceTechnologyResponse,
)
def update_experience_technology(
    experience_id: int,
    technology_id: int,
    payload: ExperienceTechnologyUpdate,
    service: ProfessionalService = Depends(
        get_professional_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.update_technology(
        experience_id,
        technology_id,
        payload,
    )


@router.delete(
    "/experiences/{experience_id}/technologies/{technology_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_experience_technology(
    experience_id: int,
    technology_id: int,
    service: ProfessionalService = Depends(
        get_professional_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    service.remove_technology(
        experience_id,
        technology_id,
    )

    return Response(
        status_code=204
    )


# EDUCATION

@router.get(
    "/educations",
    response_model=EducationListResponse,
)
def get_educations(
    service: ProfessionalService = Depends(
        get_professional_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    items, total = service.get_educations()

    return EducationListResponse(
        items=items,
        total=total,
    )


@router.post(
    "/educations",
    response_model=EducationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_education(
    payload: EducationCreate,
    service: ProfessionalService = Depends(
        get_professional_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.create_education(
        payload
    )


@router.patch(
    "/educations/{education_id}",
    response_model=EducationResponse,
)
def update_education(
    education_id: int,
    payload: EducationUpdate,
    service: ProfessionalService = Depends(
        get_professional_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.update_education(
        education_id,
        payload,
    )


@router.delete(
    "/educations/{education_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_education(
    education_id: int,
    service: ProfessionalService = Depends(
        get_professional_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    service.delete_education(
        education_id
    )

    return Response(
        status_code=204
    )