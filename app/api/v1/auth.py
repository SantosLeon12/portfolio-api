from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.api.dependencies.auth import (
    get_current_admin,
)
from app.core.exceptions import (
    InactiveAdminError,
    InvalidCredentialsError,
)
from app.database.dependencies import get_db
from app.models.admin_user import AdminUser
from app.repositories.admin_user_repository import (
    AdminUserRepository,
)
from app.schemas.auth import (
    AdminUserResponse,
    LoginRequest,
    LoginResponse,
)
from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


def get_auth_service(
    db: Session = Depends(get_db),
) -> AuthService:
    repository = AdminUserRepository(db)

    return AuthService(
        repository=repository,
    )


@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(
    payload: LoginRequest,
    service: AuthService = Depends(
        get_auth_service
    ),
):
    try:
        admin_user, access_token = service.login(
            email=str(payload.email),
            password=payload.password,
        )

    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    except InactiveAdminError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin user is inactive",
        )

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=service.access_token_expire_seconds,
        admin=admin_user,
    )


@router.get(
    "/me",
    response_model=AdminUserResponse,
)
def get_me(
    current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return current_admin