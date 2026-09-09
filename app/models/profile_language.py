from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.language import Language
    from app.models.profile import Profile
    from app.models.proficiency_level import ProficiencyLevel

class ProfileLanguage(Base):
    __tablename__ = "profile_languages"

    __table_args__ = (
        CheckConstraint(
            "display_order >= 0",
            name="display_order_non_negative",
        ),
    )

    profile_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "profiles.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    language_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "languages.id",
            ondelete="RESTRICT",
        ),
        primary_key=True,
    )

    proficiency_level_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "proficiency_levels.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    display_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default="0",
    )
    profile: Mapped["Profile"] = relationship(
    back_populates="languages",
    )

    language: Mapped["Language"] = relationship(
        back_populates="profile_languages",
    )

    proficiency_level: Mapped["ProficiencyLevel"] = relationship(
        back_populates="profile_languages",
    )