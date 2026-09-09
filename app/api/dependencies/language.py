from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.repositories.language_repository import (
    LanguageRepository,
)
from app.services.language_service import (
    LanguageService,
)


def get_language_service(
    db: Session = Depends(get_db),
):
    return LanguageService(
        LanguageRepository(db)
    )