from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Identity,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column,relationship

from app.database.base import Base
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.technology import Technology

class TechnologyCategory(TimestampMixin, Base):
    __tablename__ = "technology_categories"

    __table_args__ = (
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

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )

    slug: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )

    display_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default="0",
    )
    technologies: Mapped[list["Technology"]] = relationship(
        back_populates="category",
        passive_deletes="all",
    )