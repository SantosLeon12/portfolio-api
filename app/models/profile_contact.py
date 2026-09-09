from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    ForeignKey,
    Identity,
    Index,
    Integer,
    String,
    UniqueConstraint,
    text,
    true,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.profile import Profile

class ProfileContact(TimestampMixin, Base):
    __tablename__ = "profile_contacts"

    __table_args__ = (
        CheckConstraint(
            """
            contact_type IN (
                'EMAIL',
                'PHONE',
                'WHATSAPP',
                'OTHER'
            )
            """,
            name="contact_type",
        ),
        CheckConstraint(
            "display_order >= 0",
            name="display_order_non_negative",
        ),
        UniqueConstraint(
            "profile_id",
            "contact_type",
            "value",
            name="profile_contact",
        ),
        Index(
            "uq_profile_contacts_primary_type",
            "profile_id",
            "contact_type",
            unique=True,
            postgresql_where=text("is_primary = true"),
        ),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )

    profile_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "profiles.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    contact_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    label: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    value: Mapped[str] = mapped_column(
        String(320),
        nullable=False,
    )

    is_primary: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default="false",
    )

    display_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default="0",
    )

    is_visible: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=true(),
    )
    profile: Mapped["Profile"] = relationship(
        back_populates="contacts",
    )