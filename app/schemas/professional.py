from datetime import date, datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from app.schemas.organization import OrganizationResponse
from app.schemas.technology import TechnologyResponse


# =========================================================
# EXPERIENCE HIGHLIGHTS
# =========================================================

class ExperienceHighlightCreate(BaseModel):
    content: str = Field(min_length=1)
    display_order: int = Field(default=0, ge=0)
    is_visible: bool = True


class ExperienceHighlightUpdate(BaseModel):
    content: str | None = Field(
        default=None,
        min_length=1,
    )

    display_order: int | None = Field(
        default=None,
        ge=0,
    )

    is_visible: bool | None = None


class ExperienceHighlightResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    content: str
    display_order: int
    is_visible: bool


# =========================================================
# EXPERIENCE TECHNOLOGIES
# =========================================================

class ExperienceTechnologyCreate(BaseModel):
    technology_id: int

    display_order: int = Field(
        default=0,
        ge=0,
    )


class ExperienceTechnologyUpdate(BaseModel):
    display_order: int = Field(
        ge=0,
    )


class ExperienceTechnologyResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    display_order: int
    technology: TechnologyResponse


# =========================================================
# EXPERIENCES
# =========================================================

class ExperienceCreate(BaseModel):
    organization_id: int

    role_title: str = Field(
        min_length=1,
        max_length=160,
    )

    employment_type: str | None = Field(
        default=None,
        max_length=60,
    )

    location: str | None = Field(
        default=None,
        max_length=160,
    )

    start_date: date
    end_date: date | None = None

    summary: str | None = None

    display_order: int = Field(
        default=0,
        ge=0,
    )

    is_visible: bool = True


class ExperienceUpdate(BaseModel):
    organization_id: int | None = None

    role_title: str | None = Field(
        default=None,
        min_length=1,
        max_length=160,
    )

    employment_type: str | None = Field(
        default=None,
        max_length=60,
    )

    location: str | None = Field(
        default=None,
        max_length=160,
    )

    start_date: date | None = None
    end_date: date | None = None

    summary: str | None = None

    display_order: int | None = Field(
        default=None,
        ge=0,
    )

    is_visible: bool | None = None


class ExperienceResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    organization_id: int
    organization: OrganizationResponse

    role_title: str
    employment_type: str | None
    location: str | None

    start_date: date
    end_date: date | None

    summary: str | None
    display_order: int
    is_visible: bool

    highlights: list[
        ExperienceHighlightResponse
    ]

    technologies: list[
        ExperienceTechnologyResponse
    ]

    created_at: datetime
    updated_at: datetime


class ExperienceListResponse(BaseModel):
    items: list[ExperienceResponse]
    total: int


# =========================================================
# EDUCATION
# =========================================================

class EducationCreate(BaseModel):
    organization_id: int

    degree: str = Field(
        min_length=1,
        max_length=180,
    )

    field_of_study: str | None = Field(
        default=None,
        max_length=180,
    )

    location: str | None = Field(
        default=None,
        max_length=160,
    )

    start_date: date
    end_date: date | None = None

    description: str | None = None

    display_order: int = Field(
        default=0,
        ge=0,
    )

    is_visible: bool = True


class EducationUpdate(BaseModel):
    organization_id: int | None = None

    degree: str | None = Field(
        default=None,
        min_length=1,
        max_length=180,
    )

    field_of_study: str | None = Field(
        default=None,
        max_length=180,
    )

    location: str | None = Field(
        default=None,
        max_length=160,
    )

    start_date: date | None = None
    end_date: date | None = None

    description: str | None = None

    display_order: int | None = Field(
        default=None,
        ge=0,
    )

    is_visible: bool | None = None


class EducationResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    organization_id: int
    organization: OrganizationResponse

    degree: str
    field_of_study: str | None
    location: str | None

    start_date: date
    end_date: date | None

    description: str | None

    display_order: int
    is_visible: bool

    created_at: datetime
    updated_at: datetime


class EducationListResponse(BaseModel):
    items: list[EducationResponse]
    total: int