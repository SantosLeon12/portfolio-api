from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import BigInteger, Identity, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.profile_language import ProfileLanguage

class Language(Base):
    __tablename__ = "languages"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
        unique=True,
    )

    iso_code: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        unique=True,
    )

    profile_languages: Mapped[list["ProfileLanguage"]] = relationship(
        back_populates="language",
        passive_deletes=True,
    )