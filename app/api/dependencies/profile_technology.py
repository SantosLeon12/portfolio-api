from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.repositories.profile_technology_repository import (
    ProfileTechnologyRepository,
)
from app.services.profile_technology_service import (
    ProfileTechnologyService,
)


def get_profile_technology_service(
    db: Session = Depends(get_db),
):
    return ProfileTechnologyService(
        ProfileTechnologyRepository(db)
    )