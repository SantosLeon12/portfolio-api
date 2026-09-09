from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    ForeignKey,
    Identity,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.media_asset import MediaAsset
    from app.models.profile import Profile

class ProfileMedia(Base):
    __tablename__ = "profile_media"

    __table_args__ = (
        CheckConstraint(
            """
            media_role IN (
                'AVATAR',
                'HERO',
                'ABOUT',
                'BACKGROUND',
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
            "profile_id",
            "media_asset_id",
            name="profile_media_asset",
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

    media_role: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    alt_text: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    display_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default="0",
    )
    profile: Mapped["Profile"] = relationship(
        back_populates="media",
    )

    media_asset: Mapped["MediaAsset"] = relationship(
        back_populates="profile_media",
    )