from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.repositories.technology_repository import (
    TechnologyRepository,
)
from app.services.technology_service import (
    TechnologyService,
)


def get_technology_service(
    db: Session = Depends(get_db),
) -> TechnologyService:
    repository = TechnologyRepository(db)

    return TechnologyService(
        repository=repository,
    )