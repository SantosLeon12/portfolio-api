from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class OrganizationBase(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=180,
    )

    slug: str = Field(
        min_length=1,
        max_length=180,
    )

    organization_type: str = Field(
        min_length=1,
        max_length=30,
    )

    website_url: str | None = None

    logo_media_id: int | None = None


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=180,
    )

    slug: str | None = Field(
        default=None,
        min_length=1,
        max_length=180,
    )

    organization_type: str | None = Field(
        default=None,
        min_length=1,
        max_length=30,
    )

    website_url: str | None = None
    logo_media_id: int | None = None


class OrganizationResponse(OrganizationBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    created_at: datetime
    updated_at: datetime


class OrganizationListResponse(BaseModel):
    items: list[OrganizationResponse]
    total: int