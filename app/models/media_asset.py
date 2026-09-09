from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Identity,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

from datetime import datetime

from sqlalchemy import DateTime, func

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.profile_document import ProfileDocument
    from app.models.profile_media import ProfileMedia
    from app.models.project_media import ProjectMedia
    from app.models.technology import Technology

class MediaAsset(Base):
    __tablename__ = "media_assets"

    __table_args__ = (
        UniqueConstraint(
            "storage_provider",
            "storage_key",
            name="storage_provider_key",
        ),
        CheckConstraint(
            "file_size IS NULL OR file_size >= 0",
            name="file_size_non_negative",
        ),
        CheckConstraint(
            "width IS NULL OR width > 0",
            name="width_positive",
        ),
        CheckConstraint(
            "height IS NULL OR height > 0",
            name="height_positive",
        ),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )

    storage_provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    storage_key: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    mime_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    file_size: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True,
    )

    width: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    height: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    profile_media: Mapped[list["ProfileMedia"]] = relationship(
        back_populates="media_asset",
        passive_deletes=True,
    )

    profile_documents: Mapped[list["ProfileDocument"]] = relationship(
        back_populates="media_asset",
        passive_deletes=True,
    )

    organization_logos: Mapped[list["Organization"]] = relationship(
        back_populates="logo_media",
        passive_deletes=True,
    )
    technology_icons: Mapped[list["Technology"]] = relationship(
        back_populates="icon_media",
        passive_deletes=True,
    )

    project_media: Mapped[list["ProjectMedia"]] = relationship(
        back_populates="media_asset",
        passive_deletes=True,
    )