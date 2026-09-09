from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    ForeignKey,
    Identity,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.education import Education
    from app.models.experience import Experience
    from app.models.media_asset import MediaAsset
    from app.models.project import Project

class Organization(TimestampMixin, Base):
    __tablename__ = "organizations"

    __table_args__ = (
        CheckConstraint(
            """
            organization_type IN (
                'COMPANY',
                'UNIVERSITY',
                'SCHOOL',
                'CLIENT',
                'OTHER'
            )
            """,
            name="organization_type",
        ),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(180),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(180),
        nullable=False,
        unique=True,
        index=True,
    )

    organization_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    website_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    logo_media_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey(
            "media_assets.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )
    experiences: Mapped[list["Experience"]] = relationship(
        back_populates="organization",
        passive_deletes="all",
    )

    educations: Mapped[list["Education"]] = relationship(
        back_populates="organization",
        passive_deletes="all",
    )
    logo_media: Mapped["MediaAsset | None"] = relationship(
        back_populates="organization_logos",
    )
    projects: Mapped[list["Project"]] = relationship(
        back_populates="organization",
        passive_deletes=True,
    )