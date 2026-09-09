from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)


class ContactMessageCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=160,
    )

    email: EmailStr

    subject: str = Field(
        min_length=1,
        max_length=200,
    )

    message: str = Field(
        min_length=1,
        max_length=5000,
    )


class ContactMessageStatusUpdate(BaseModel):
    status: str


class ContactMessageResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    name: str
    email: EmailStr
    subject: str
    message: str

    status: str

    created_at: datetime
    read_at: datetime | None


class ContactMessageListResponse(BaseModel):
    items: list[
        ContactMessageResponse
    ]

    total: int