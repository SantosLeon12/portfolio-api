from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Identity,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.profile_language import ProfileLanguage

class ProficiencyLevel(Base):
    __tablename__ = "proficiency_levels"

    __table_args__ = (
        CheckConstraint(
            "rank > 0",
            name="rank_positive",
        ),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )

    code: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
    )

    name: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )

    rank: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        unique=True,
    )
    profile_languages: Mapped[list["ProfileLanguage"]] = relationship(
        back_populates="proficiency_level",
        passive_deletes="all",
    )