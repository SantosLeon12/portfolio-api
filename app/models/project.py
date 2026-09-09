from __future__ import annotations

from typing import TYPE_CHECKING
from datetime import date, datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Identity,
    Integer,
    String,
    Text,
    false,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.profile import Profile
    from app.models.project_category_relation import ProjectCategoryRelation
    from app.models.project_link import ProjectLink
    from app.models.project_media import ProjectMedia
    from app.models.project_section import ProjectSection
    from app.models.project_technology import ProjectTechnology

class Project(TimestampMixin, Base):
    __tablename__ = "projects"

    __table_args__ = (
        CheckConstraint(
            """
            status IN (
                'DRAFT',
                'PUBLISHED',
                'ARCHIVED'
            )
            """,
            name="status",
        ),
        CheckConstraint(
            """
            end_date IS NULL
            OR start_date IS NULL
            OR end_date >= start_date
            """,
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

    organization_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey(
            "organizations.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(180),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(180),
        nullable=False,
        unique=True,
        index=True,
    )

    short_description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    overview: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    role_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    start_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        server_default="DRAFT",
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

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    profile: Mapped["Profile"] = relationship(
        back_populates="projects",
    )

    organization: Mapped["Organization | None"] = relationship(
        back_populates="projects",
    )

    categories: Mapped[list["ProjectCategoryRelation"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    technologies: Mapped[list["ProjectTechnology"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="ProjectTechnology.display_order",
    )

    links: Mapped[list["ProjectLink"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="ProjectLink.display_order",
    )

    media: Mapped[list["ProjectMedia"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="ProjectMedia.display_order",
    )

    sections: Mapped[list["ProjectSection"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="ProjectSection.display_order",
    )