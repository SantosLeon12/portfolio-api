from datetime import date, datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from app.schemas.media import (
    MediaAssetResponse,
)
from app.schemas.organization import (
    OrganizationResponse,
)
from app.schemas.technology import (
    TechnologyResponse,
)


# =========================================================
# CATEGORY
# =========================================================

class ProjectCategoryCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=120,
    )

    slug: str = Field(
        min_length=1,
        max_length=120,
    )

    display_order: int = Field(
        default=0,
        ge=0,
    )


class ProjectCategoryUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=120,
    )

    slug: str | None = Field(
        default=None,
        min_length=1,
        max_length=120,
    )

    display_order: int | None = Field(
        default=None,
        ge=0,
    )


class ProjectCategoryResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    name: str
    slug: str
    display_order: int

    created_at: datetime
    updated_at: datetime


class ProjectCategoryRelationResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    category: ProjectCategoryResponse


# =========================================================
# TECHNOLOGY
# =========================================================

class ProjectTechnologyCreate(BaseModel):
    technology_id: int

    display_order: int = Field(
        default=0,
        ge=0,
    )


class ProjectTechnologyUpdate(BaseModel):
    display_order: int = Field(
        ge=0,
    )


class ProjectTechnologyResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    display_order: int
    technology: TechnologyResponse


# =========================================================
# LINK
# =========================================================

class ProjectLinkCreate(BaseModel):
    link_type: str
    label: str | None = None
    url: str = Field(min_length=1)

    display_order: int = Field(
        default=0,
        ge=0,
    )

    is_visible: bool = True


class ProjectLinkUpdate(BaseModel):
    link_type: str | None = None
    label: str | None = None
    url: str | None = Field(
        default=None,
        min_length=1,
    )

    display_order: int | None = Field(
        default=None,
        ge=0,
    )

    is_visible: bool | None = None


class ProjectLinkResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    link_type: str
    label: str | None
    url: str

    display_order: int
    is_visible: bool


# =========================================================
# MEDIA
# =========================================================

class ProjectMediaCreate(BaseModel):
    media_asset_id: int
    media_role: str

    alt_text: str | None = None
    caption: str | None = None

    display_order: int = Field(
        default=0,
        ge=0,
    )

    is_visible: bool = True


class ProjectMediaUpdate(BaseModel):
    media_role: str | None = None

    alt_text: str | None = None
    caption: str | None = None

    display_order: int | None = Field(
        default=None,
        ge=0,
    )

    is_visible: bool | None = None


class ProjectMediaResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    media_role: str
    alt_text: str | None
    caption: str | None

    display_order: int
    is_visible: bool

    media_asset: MediaAssetResponse


# =========================================================
# SECTION ITEMS
# =========================================================

class ProjectSectionItemCreate(BaseModel):
    content: str = Field(min_length=1)

    display_order: int = Field(
        default=0,
        ge=0,
    )

    is_visible: bool = True


class ProjectSectionItemUpdate(BaseModel):
    content: str | None = Field(
        default=None,
        min_length=1,
    )

    display_order: int | None = Field(
        default=None,
        ge=0,
    )

    is_visible: bool | None = None


class ProjectSectionItemResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    content: str
    display_order: int
    is_visible: bool


# =========================================================
# SECTIONS
# =========================================================

class ProjectSectionCreate(BaseModel):
    section_type: str

    title: str | None = None
    body: str | None = None

    display_order: int = Field(
        default=0,
        ge=0,
    )

    is_visible: bool = True


class ProjectSectionUpdate(BaseModel):
    section_type: str | None = None
    title: str | None = None
    body: str | None = None

    display_order: int | None = Field(
        default=None,
        ge=0,
    )

    is_visible: bool | None = None


class ProjectSectionResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    section_type: str
    title: str | None
    body: str | None

    display_order: int
    is_visible: bool

    items: list[
        ProjectSectionItemResponse
    ]


# =========================================================
# PROJECT
# =========================================================

class ProjectCreate(BaseModel):
    organization_id: int | None = None

    title: str = Field(
        min_length=1,
        max_length=180,
    )

    slug: str = Field(
        min_length=1,
        max_length=180,
    )

    short_description: str | None = None
    overview: str | None = None
    role_summary: str | None = None

    start_date: date | None = None
    end_date: date | None = None

    status: str = "DRAFT"
    featured: bool = False

    display_order: int = Field(
        default=0,
        ge=0,
    )


class ProjectUpdate(BaseModel):
    organization_id: int | None = None

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=180,
    )

    slug: str | None = Field(
        default=None,
        min_length=1,
        max_length=180,
    )

    short_description: str | None = None
    overview: str | None = None
    role_summary: str | None = None

    start_date: date | None = None
    end_date: date | None = None

    status: str | None = None
    featured: bool | None = None

    display_order: int | None = Field(
        default=None,
        ge=0,
    )


class ProjectResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    organization_id: int | None
    organization: OrganizationResponse | None

    title: str
    slug: str

    short_description: str | None
    overview: str | None
    role_summary: str | None

    start_date: date | None
    end_date: date | None

    status: str
    featured: bool
    display_order: int

    published_at: datetime | None

    categories: list[
        ProjectCategoryRelationResponse
    ]

    technologies: list[
        ProjectTechnologyResponse
    ]

    links: list[
        ProjectLinkResponse
    ]

    media: list[
        ProjectMediaResponse
    ]

    sections: list[
        ProjectSectionResponse
    ]

    created_at: datetime
    updated_at: datetime


class ProjectListResponse(BaseModel):
    items: list[ProjectResponse]
    total: int