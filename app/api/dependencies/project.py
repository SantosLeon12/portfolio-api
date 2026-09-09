from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.repositories.project_repository import (
    ProjectRepository,
)
from app.services.project_service import (
    ProjectService,
)


def get_project_service(
    db: Session = Depends(get_db),
):
    return ProjectService(
        ProjectRepository(db)
    )