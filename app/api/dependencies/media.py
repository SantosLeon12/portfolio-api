from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.repositories.media_repository import (
    MediaRepository,
)
from app.services.media_service import (
    MediaService,
)


def get_media_service(
    db: Session = Depends(get_db),
) -> MediaService:
    return MediaService(
        MediaRepository(db)
    )