from datetime import datetime, timezone

from app.core.exceptions import (
    DomainValidationError,
    ResourceNotFoundError,
)
from app.models.contact_message import (
    ContactMessage,
)
from app.repositories.contact_repository import (
    ContactRepository,
)
from app.schemas.contact import (
    ContactMessageCreate,
)


class ContactService:
    STATUSES = {
        "NEW",
        "READ",
        "ARCHIVED",
    }

    def __init__(
        self,
        repository: ContactRepository,
    ):
        self.repository = repository

    def create(
        self,
        data: ContactMessageCreate,
    ):
        message = ContactMessage(
            name=data.name.strip(),
            email=str(data.email).lower(),
            subject=data.subject.strip(),
            message=data.message.strip(),
            status="NEW",
        )

        return self.repository.save(
            message
        )

    def get_all(
        self,
        status_filter: str | None = None,
    ):
        if status_filter is not None:
            status_filter = (
                status_filter.upper()
            )

            if (
                status_filter
                not in self.STATUSES
            ):
                raise DomainValidationError(
                    "Invalid contact message status"
                )

        items = self.repository.get_all(
            status_filter
        )

        total = self.repository.count(
            status_filter
        )

        return items, total

    def get(
        self,
        message_id: int,
    ):
        message = self.repository.get(
            message_id
        )

        if message is None:
            raise ResourceNotFoundError(
                "Contact message not found"
            )

        return message

    def update_status(
        self,
        message_id: int,
        new_status: str,
    ):
        message = self.get(message_id)

        new_status = new_status.upper()

        if new_status not in self.STATUSES:
            raise DomainValidationError(
                "Invalid contact message status"
            )

        message.status = new_status

        if new_status == "READ":
            if message.read_at is None:
                message.read_at = (
                    datetime.now(
                        timezone.utc
                    )
                )

        if new_status == "NEW":
            message.read_at = None

        return self.repository.save(
            message
        )

    def delete(
        self,
        message_id: int,
    ):
        message = self.get(message_id)

        self.repository.delete(
            message
        )