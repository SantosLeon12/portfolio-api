from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)


# =========================================================
# PROFILE
# =========================================================

class ProfileBase(BaseModel):
    full_name: str = Field(
        min_length=1,
        max_length=160,
    )

    professional_title: str = Field(
        min_length=1,
        max_length=120,
    )

    headline: str | None = Field(
        default=None,
        max_length=255,
    )

    short_bio: str | None = None
    about: str | None = None
    mission: str | None = None

    location: str | None = Field(
        default=None,
        max_length=160,
    )

    availability_text: str | None = Field(
        default=None,
        max_length=255,
    )


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(BaseModel):
    full_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=160,
    )

    professional_title: str | None = Field(
        default=None,
        min_length=1,
        max_length=120,
    )

    headline: str | None = Field(
        default=None,
        max_length=255,
    )

    short_bio: str | None = None
    about: str | None = None
    mission: str | None = None

    location: str | None = Field(
        default=None,
        max_length=160,
    )

    availability_text: str | None = Field(
        default=None,
        max_length=255,
    )


# =========================================================
# CONTACTS
# =========================================================

class ProfileContactBase(BaseModel):
    contact_type: str = Field(
        min_length=1,
        max_length=20,
    )

    label: str | None = Field(
        default=None,
        max_length=100,
    )

    value: str = Field(
        min_length=1,
        max_length=320,
    )

    is_primary: bool = False

    display_order: int = Field(
        default=0,
        ge=0,
    )

    is_visible: bool = True


class ProfileContactCreate(ProfileContactBase):
    pass


class ProfileContactUpdate(BaseModel):
    contact_type: str | None = Field(
        default=None,
        min_length=1,
        max_length=20,
    )

    label: str | None = Field(
        default=None,
        max_length=100,
    )

    value: str | None = Field(
        default=None,
        min_length=1,
        max_length=320,
    )

    is_primary: bool | None = None

    display_order: int | None = Field(
        default=None,
        ge=0,
    )

    is_visible: bool | None = None


class ProfileContactResponse(ProfileContactBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int


# =========================================================
# SOCIAL LINKS
# =========================================================

class SocialLinkBase(BaseModel):
    platform: str = Field(
        min_length=1,
        max_length=60,
    )

    label: str | None = Field(
        default=None,
        max_length=100,
    )

    url: str = Field(
        min_length=1,
    )

    display_order: int = Field(
        default=0,
        ge=0,
    )

    is_visible: bool = True


class SocialLinkCreate(SocialLinkBase):
    pass


class SocialLinkUpdate(BaseModel):
    platform: str | None = Field(
        default=None,
        min_length=1,
        max_length=60,
    )

    label: str | None = Field(
        default=None,
        max_length=100,
    )

    url: str | None = Field(
        default=None,
        min_length=1,
    )

    display_order: int | None = Field(
        default=None,
        ge=0,
    )

    is_visible: bool | None = None


class SocialLinkResponse(SocialLinkBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int


# =========================================================
# STRENGTHS
# =========================================================

class StrengthBase(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=120,
    )

    description: str | None = None

    display_order: int = Field(
        default=0,
        ge=0,
    )

    is_visible: bool = True


class StrengthCreate(StrengthBase):
    pass


class StrengthUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=120,
    )

    description: str | None = None

    display_order: int | None = Field(
        default=None,
        ge=0,
    )

    is_visible: bool | None = None


class StrengthResponse(StrengthBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int


# =========================================================
# INTERESTS
# =========================================================

class InterestBase(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=120,
    )

    description: str | None = None

    display_order: int = Field(
        default=0,
        ge=0,
    )

    is_visible: bool = True


class InterestCreate(InterestBase):
    pass


class InterestUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=120,
    )

    description: str | None = None

    display_order: int | None = Field(
        default=None,
        ge=0,
    )

    is_visible: bool | None = None


class InterestResponse(InterestBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int


# =========================================================
# PROFILE RESPONSE
# =========================================================

class ProfileResponse(ProfileBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    contacts: list[ProfileContactResponse]
    social_links: list[SocialLinkResponse]
    strengths: list[StrengthResponse]
    interests: list[InterestResponse]

    created_at: datetime
    updated_at: datetime