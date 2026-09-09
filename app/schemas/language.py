from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class LanguageCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=80,
    )

    iso_code: str = Field(
        min_length=2,
        max_length=10,
    )


class LanguageUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=80,
    )

    iso_code: str | None = Field(
        default=None,
        min_length=2,
        max_length=10,
    )


class LanguageResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    name: str
    iso_code: str


class ProficiencyLevelCreate(BaseModel):
    code: str = Field(
        min_length=1,
        max_length=20,
    )

    name: str = Field(
        min_length=1,
        max_length=80,
    )

    rank: int = Field(ge=1)


class ProficiencyLevelUpdate(BaseModel):
    code: str | None = Field(
        default=None,
        min_length=1,
        max_length=20,
    )

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=80,
    )

    rank: int | None = Field(
        default=None,
        ge=1,
    )


class ProficiencyLevelResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    code: str
    name: str
    rank: int


class ProfileLanguageCreate(BaseModel):
    language_id: int
    proficiency_level_id: int

    display_order: int = Field(
        default=0,
        ge=0,
    )


class ProfileLanguageUpdate(BaseModel):
    proficiency_level_id: int | None = None

    display_order: int | None = Field(
        default=None,
        ge=0,
    )


class ProfileLanguageResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    display_order: int

    language: LanguageResponse

    proficiency_level: (
        ProficiencyLevelResponse
    )


class ProfileLanguageListResponse(BaseModel):
    items: list[
        ProfileLanguageResponse
    ]

    total: int