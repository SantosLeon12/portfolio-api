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
    UniqueConstraint,
    true,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.media_asset import MediaAsset
    from app.models.project import Project

class ProjectMedia(Base):
    __tablename__ = "project_media"

    __table_args__ = (
        CheckConstraint(
            """
            media_role IN (
                'COVER',
                'SCREENSHOT',
                'GALLERY',
                'DIAGRAM',
                'LOGO',
                'OTHER'
            )
            """,
            name="media_role",
        ),
        CheckConstraint(
            "display_order >= 0",
            name="display_order_non_negative",
        ),
        UniqueConstraint(
            "project_id",
            "media_asset_id",
            name="project_media_asset",
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

    media_asset_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "media_assets.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    media_role: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    alt_text: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    caption: Mapped[str | None] = mapped_column(
        String(500),
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
        back_populates="media",
    )

    media_asset: Mapped["MediaAsset"] = relationship(
        back_populates="project_media",
    )