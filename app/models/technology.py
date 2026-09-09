from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import (
    BigInteger,
    ForeignKey,
    Identity,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.experience_technology import ExperienceTechnology
    from app.models.media_asset import MediaAsset
    from app.models.profile_technology import ProfileTechnology
    from app.models.project_technology import ProjectTechnology
    from app.models.technology_category import TechnologyCategory

class Technology(TimestampMixin, Base):
    __tablename__ = "technologies"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )

    technology_category_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "technology_categories.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        unique=True,
    )

    slug: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        unique=True,
    )

    official_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    icon_media_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey(
            "media_assets.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )
    category: Mapped["TechnologyCategory"] = relationship(
        back_populates="technologies",
    )

    icon_media: Mapped["MediaAsset | None"] = relationship(
        back_populates="technology_icons",
    )

    profile_technologies: Mapped[list["ProfileTechnology"]] = relationship(
        back_populates="technology",
        passive_deletes=True,
    )

    experience_technologies: Mapped[list["ExperienceTechnology"]] = relationship(
        back_populates="technology",
        passive_deletes=True,
    )

    project_technologies: Mapped[list["ProjectTechnology"]] = relationship(
        back_populates="technology",
        passive_deletes=True,
    )