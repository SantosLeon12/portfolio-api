from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    ForeignKey,
    Integer,
    false,
    true,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.profile import Profile
    from app.models.technology import Technology

class ProfileTechnology(Base):
    __tablename__ = "profile_technologies"

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

    technology_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "technologies.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    featured: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=false(),
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
        back_populates="technologies",
    )

    technology: Mapped["Technology"] = relationship(
        back_populates="profile_technologies",
    )