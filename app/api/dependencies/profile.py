from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.repositories.profile_repository import (
    ProfileRepository,
)
from app.services.profile_service import (
    ProfileService,
)


def get_profile_service(
    db: Session = Depends(get_db),
) -> ProfileService:
    repository = ProfileRepository(db)

    return ProfileService(
        repository=repository,
    )