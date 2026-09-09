from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.admin_user import AdminUser


class AdminUserRepository:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def get_by_id(
        self,
        admin_user_id: int,
    ) -> AdminUser | None:
        return self.db.get(
            AdminUser,
            admin_user_id,
        )

    def get_by_email(
        self,
        email: str,
    ) -> AdminUser | None:
        statement = select(
            AdminUser
        ).where(
            AdminUser.email == email
        )

        return self.db.scalar(statement)

    def update_last_login(
        self,
        admin_user: AdminUser,
    ) -> AdminUser:
        admin_user.last_login_at = datetime.now(
            timezone.utc
        )

        self.db.add(admin_user)
        self.db.commit()
        self.db.refresh(admin_user)

        return admin_user