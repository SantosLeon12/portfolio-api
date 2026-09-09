from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.repositories.contact_repository import (
    ContactRepository,
)
from app.services.contact_service import (
    ContactService,
)


def get_contact_service(
    db: Session = Depends(get_db),
):
    return ContactService(
        ContactRepository(db)
    )