from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    ForeignKey,
    Identity,
    Integer,
    Text,
    true,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.project_section import ProjectSection

class ProjectSectionItem(Base):
    __tablename__ = "project_section_items"

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

    project_section_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "project_sections.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
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
    section: Mapped["ProjectSection"] = relationship(
        back_populates="items",
    )