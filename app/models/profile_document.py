from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    ForeignKey,
    Identity,
    Index,
    String,
    UniqueConstraint,
    text,
    true,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.media_asset import MediaAsset
    from app.models.profile import Profile

class ProfileDocument(TimestampMixin, Base):
    __tablename__ = "profile_documents"

    __table_args__ = (
        CheckConstraint(
            """
            document_type IN (
                'CV',
                'RESUME',
                'CERTIFICATE',
                'OTHER'
            )
            """,
            name="document_type",
        ),
        UniqueConstraint(
            "profile_id",
            "media_asset_id",
            name="profile_document_asset",
        ),
        Index(
            "uq_profile_documents_current_type",
            "profile_id",
            "document_type",
            unique=True,
            postgresql_where=text("is_current = true"),
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

    media_asset_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "media_assets.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    document_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(160),
        nullable=False,
    )

    version: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    is_current: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=true(),
    )
    profile: Mapped["Profile"] = relationship(
        back_populates="documents",
    )

    media_asset: Mapped["MediaAsset"] = relationship(
        back_populates="profile_documents",
    )