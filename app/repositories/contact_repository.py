from sqlalchemy import (
    func,
    select,
)
from sqlalchemy.orm import Session

from app.models.contact_message import (
    ContactMessage,
)


class ContactRepository:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def get_all(
        self,
        status_filter: str | None = None,
    ):
        statement = select(
            ContactMessage
        )

        if status_filter is not None:
            statement = statement.where(
                ContactMessage.status
                == status_filter
            )

        statement = statement.order_by(
            ContactMessage.created_at.desc()
        )

        return list(
            self.db.scalars(statement).all()
        )

    def count(
        self,
        status_filter: str | None = None,
    ):
        statement = select(
            func.count(ContactMessage.id)
        )

        if status_filter is not None:
            statement = statement.where(
                ContactMessage.status
                == status_filter
            )

        return self.db.scalar(statement) or 0

    def get(
        self,
        message_id: int,
    ):
        return self.db.get(
            ContactMessage,
            message_id,
        )

    def save(
        self,
        message: ContactMessage,
    ):
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return message

    def delete(
        self,
        message: ContactMessage,
    ):
        self.db.delete(message)
        self.db.commit()