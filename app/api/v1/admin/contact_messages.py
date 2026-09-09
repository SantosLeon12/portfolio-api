from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from app.api.dependencies.auth import (
    get_current_admin,
)
from app.api.dependencies.contact import (
    get_contact_service,
)
from app.models.admin_user import AdminUser
from app.schemas.contact import (
    ContactMessageListResponse,
    ContactMessageResponse,
    ContactMessageStatusUpdate,
)
from app.services.contact_service import (
    ContactService,
)


router = APIRouter(
    prefix="/contact-messages",
    tags=["Admin - Contact Messages"],
)


@router.get(
    "",
    response_model=ContactMessageListResponse,
)
def get_messages(
    status_filter: str | None = None,
    service: ContactService = Depends(
        get_contact_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    items, total = service.get_all(
        status_filter
    )

    return ContactMessageListResponse(
        items=items,
        total=total,
    )


@router.get(
    "/{message_id}",
    response_model=ContactMessageResponse,
)
def get_message(
    message_id: int,
    service: ContactService = Depends(
        get_contact_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.get(message_id)


@router.patch(
    "/{message_id}/status",
    response_model=ContactMessageResponse,
)
def update_message_status(
    message_id: int,
    payload: ContactMessageStatusUpdate,
    service: ContactService = Depends(
        get_contact_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.update_status(
        message_id,
        payload.status,
    )


@router.delete(
    "/{message_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_message(
    message_id: int,
    service: ContactService = Depends(
        get_contact_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    service.delete(message_id)

    return Response(status_code=204)