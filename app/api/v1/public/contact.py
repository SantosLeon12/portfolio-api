from fastapi import (
    APIRouter,
    Depends,
    status,
)

from app.api.dependencies.contact import (
    get_contact_service,
)
from app.schemas.contact import (
    ContactMessageCreate,
    ContactMessageResponse,
)
from app.services.contact_service import (
    ContactService,
)


router = APIRouter(
    prefix="/contact",
    tags=["Public - Contact"],
)


@router.post(
    "",
    response_model=ContactMessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def send_message(
    payload: ContactMessageCreate,
    service: ContactService = Depends(
        get_contact_service
    ),
):
    return service.create(payload)