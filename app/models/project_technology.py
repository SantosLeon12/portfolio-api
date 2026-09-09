from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import Mapped, mapped_column,relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.technology import Technology

class ProjectTechnology(Base):
    __tablename__ = "project_technologies"

    __table_args__ = (
        CheckConstraint(
            "display_order >= 0",
            name="display_order_non_negative",
        ),
    )

    project_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "projects.id",
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

    display_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default="0",
    )
    project: Mapped["Project"] = relationship(
        back_populates="technologies",
    )

    technology: Mapped["Technology"] = relationship(
        back_populates="project_technologies",
    )