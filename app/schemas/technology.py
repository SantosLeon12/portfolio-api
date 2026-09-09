from pydantic import BaseModel, ConfigDict, Field


class TechnologyCategoryBase(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
    )

    slug: str = Field(
        min_length=1,
        max_length=100,
    )

    display_order: int = Field(
        default=0,
        ge=0,
    )


class TechnologyCategoryCreate(TechnologyCategoryBase):
    pass


class TechnologyCategoryUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    slug: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    display_order: int | None = Field(
        default=None,
        ge=0,
    )


class TechnologyCategoryResponse(TechnologyCategoryBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

class TechnologyBase(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=120,
    )

    slug: str = Field(
        min_length=1,
        max_length=120,
    )

    official_url: str | None = None


class TechnologyCreate(TechnologyBase):
    technology_category_id: int
    icon_media_id: int | None = None


class TechnologyUpdate(BaseModel):
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

    official_url: str | None = None

    technology_category_id: int | None = None

    icon_media_id: int | None = None

class TechnologyResponse(TechnologyBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    technology_category_id: int
    icon_media_id: int | None

    category: TechnologyCategoryResponse

class TechnologyListResponse(BaseModel):
    items: list[TechnologyResponse]
    total: int

class ProfileTechnologyCreate(BaseModel):
    technology_id: int

    featured: bool = False

    display_order: int = Field(
        default=0,
        ge=0,
    )

    is_visible: bool = True


class ProfileTechnologyUpdate(BaseModel):
    featured: bool | None = None

    display_order: int | None = Field(
        default=None,
        ge=0,
    )

    is_visible: bool | None = None


class ProfileTechnologyResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    featured: bool
    display_order: int
    is_visible: bool

    technology: TechnologyResponse


class ProfileTechnologyListResponse(BaseModel):
    items: list[
        ProfileTechnologyResponse
    ]

    total: int