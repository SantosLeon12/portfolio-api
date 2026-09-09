from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.repositories.professional_repository import (
    ProfessionalRepository,
)
from app.services.professional_service import (
    ProfessionalService,
)


def get_professional_service(
    db: Session = Depends(get_db),
) -> ProfessionalService:
    repository = ProfessionalRepository(
        db
    )

    return ProfessionalService(
        repository=repository
    )