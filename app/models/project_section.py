from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
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
    from app.models.project import Project
    from app.models.project_section_item import ProjectSectionItem

class ProjectSection(TimestampMixin, Base):
    __tablename__ = "project_sections"

    __table_args__ = (
        CheckConstraint(
            """
            section_type IN (
                'OVERVIEW',
                'PROBLEM',
                'RESPONSIBILITIES',
                'SOLUTION',
                'ARCHITECTURE',
                'CHALLENGES',
                'RESULTS',
                'LEARNINGS',
                'CUSTOM'
            )
            """,
            name="section_type",
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

    project_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "projects.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    section_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(160),
        nullable=False,
    )

    body: Mapped[str | None] = mapped_column(
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
    project: Mapped["Project"] = relationship(
        back_populates="sections",
    )

    items: Mapped[list["ProjectSectionItem"]] = relationship(
        back_populates="section",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="ProjectSectionItem.display_order",
    )