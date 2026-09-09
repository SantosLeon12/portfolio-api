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
    UniqueConstraint,
    true,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.project import Project

class ProjectLink(TimestampMixin, Base):
    __tablename__ = "project_links"

    __table_args__ = (
        CheckConstraint(
            """
            link_type IN (
                'REPOSITORY',
                'LIVE_DEMO',
                'DOCUMENTATION',
                'CASE_STUDY',
                'OTHER'
            )
            """,
            name="link_type",
        ),
        CheckConstraint(
            "display_order >= 0",
            name="display_order_non_negative",
        ),
        UniqueConstraint(
            "project_id",
            "url",
            name="project_url",
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

    link_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    label: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    url: Mapped[str] = mapped_column(
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
    project: Mapped["Project"] = relationship(
        back_populates="links",
    )