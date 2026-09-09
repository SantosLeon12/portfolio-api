from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.database.dependencies import get_db
from app.models.admin_user import AdminUser
from app.repositories.admin_user_repository import (
    AdminUserRepository,
)


bearer_scheme = HTTPBearer(
    auto_error=False,
)


def get_current_admin(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db),
) -> AdminUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )

    if credentials is None:
        raise credentials_exception

    token = credentials.credentials

    try:
        payload = decode_access_token(token)

    except InvalidTokenError:
        raise credentials_exception

    if payload.get("type") != "access":
        raise credentials_exception

    subject = payload.get("sub")

    if subject is None:
        raise credentials_exception

    try:
        admin_user_id = int(subject)

    except (TypeError, ValueError):
        raise credentials_exception

    repository = AdminUserRepository(db)

    admin_user = repository.get_by_id(
        admin_user_id
    )

    if admin_user is None:
        raise credentials_exception

    if not admin_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin user is inactive",
        )

    return admin_user