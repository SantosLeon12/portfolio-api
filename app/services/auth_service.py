from app.core.config import settings
from app.core.exceptions import (
    InactiveAdminError,
    InvalidCredentialsError,
)
from app.core.security import (
    create_access_token,
    verify_password,
)
from app.models.admin_user import AdminUser
from app.repositories.admin_user_repository import (
    AdminUserRepository,
)


class AuthService:
    def __init__(
        self,
        repository: AdminUserRepository,
    ):
        self.repository = repository

    def login(
        self,
        email: str,
        password: str,
    ) -> tuple[AdminUser, str]:
        normalized_email = email.strip().lower()

        admin_user = self.repository.get_by_email(
            normalized_email
        )

        if admin_user is None:
            raise InvalidCredentialsError()

        if not verify_password(
            password,
            admin_user.password_hash,
        ):
            raise InvalidCredentialsError()

        if not admin_user.is_active:
            raise InactiveAdminError()

        admin_user = (
            self.repository.update_last_login(
                admin_user
            )
        )

        access_token = create_access_token(
            subject=str(admin_user.id)
        )

        return admin_user, access_token

    @property
    def access_token_expire_seconds(self) -> int:
        return (
            settings.jwt_access_token_expire_minutes
            * 60
        )