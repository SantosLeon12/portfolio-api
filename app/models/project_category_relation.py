from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.project_category import ProjectCategory

class ProjectCategoryRelation(Base):
    __tablename__ = "project_category_relations"

    project_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "projects.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    category_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "project_categories.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
    project: Mapped["Project"] = relationship(
        back_populates="categories",
    )

    category: Mapped["ProjectCategory"] = relationship(
        back_populates="project_relations",
    )