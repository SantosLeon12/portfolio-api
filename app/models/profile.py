from __future__ import annotations
from sqlalchemy import BigInteger, Identity, String, Text

from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.education import Education
    from app.models.experience import Experience
    from app.models.interest import Interest
    from app.models.profile_contact import ProfileContact
    from app.models.profile_document import ProfileDocument
    from app.models.profile_media import ProfileMedia
    from app.models.social_link import SocialLink
    from app.models.strength import Strength
    from app.models.profile_language import ProfileLanguage
    from app.models.profile_technology import ProfileTechnology
    from app.models.project import Project

class Profile(TimestampMixin, Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(160),
        nullable=False,
    )

    professional_title: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    headline: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    short_bio: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    about: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    mission: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    location: Mapped[str | None] = mapped_column(
        String(160),
        nullable=True,
    )

    availability_text: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    experiences: Mapped[list["Experience"]] = relationship(
        back_populates="profile",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    educations: Mapped[list["Education"]] = relationship(
        back_populates="profile",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    contacts: Mapped[list["ProfileContact"]] = relationship(
        back_populates="profile",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="ProfileContact.display_order",
    )

    social_links: Mapped[list["SocialLink"]] = relationship(
        back_populates="profile",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="SocialLink.display_order",
    )

    strengths: Mapped[list["Strength"]] = relationship(
        back_populates="profile",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="Strength.display_order",
    )

    interests: Mapped[list["Interest"]] = relationship(
        back_populates="profile",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="Interest.display_order",
    )

    media: Mapped[list["ProfileMedia"]] = relationship(
        back_populates="profile",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="ProfileMedia.display_order",
    )

    documents: Mapped[list["ProfileDocument"]] = relationship(
        back_populates="profile",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="ProfileDocument.created_at",
    )
    languages: Mapped[list["ProfileLanguage"]] = relationship(
        back_populates="profile",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="ProfileLanguage.display_order",
    )
    technologies: Mapped[list["ProfileTechnology"]] = relationship(
        back_populates="profile",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="ProfileTechnology.display_order",
    )
    projects: Mapped[list["Project"]] = relationship(
        back_populates="profile",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="Project.display_order",
    )