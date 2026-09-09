from __future__ import annotations

from typing import TYPE_CHECKING
from datetime import date

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    Date,
    ForeignKey,
    Identity,
    Integer,
    String,
    Text,
    true,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.experience_highlight import ExperienceHighlight
    from app.models.organization import Organization
    from app.models.profile import Profile
    from app.models.experience_technology import ExperienceTechnology

class Experience(TimestampMixin, Base):
    __tablename__ = "experiences"

    __table_args__ = (
        CheckConstraint(
            "end_date IS NULL OR end_date >= start_date",
            name="valid_date_range",
        ),
        CheckConstraint(
            "display_order >= 0",
            name="display_order_non_negative",
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

    organization_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "organizations.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    role_title: Mapped[str] = mapped_column(
        String(160),
        nullable=False,
    )

    employment_type: Mapped[str | None] = mapped_column(
        String(60),
        nullable=True,
    )

    location: Mapped[str | None] = mapped_column(
        String(160),
        nullable=True,
    )

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
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
        back_populates="experiences",
    )

    organization: Mapped["Organization"] = relationship(
        back_populates="experiences",
    )

    highlights: Mapped[list["ExperienceHighlight"]] = relationship(
        back_populates="experience",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="ExperienceHighlight.display_order",
    )
    technologies: Mapped[list["ExperienceTechnology"]] = relationship(
        back_populates="experience",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="ExperienceTechnology.display_order",
    )