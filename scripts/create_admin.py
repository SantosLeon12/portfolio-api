from getpass import getpass

from sqlalchemy import select

from app.core.security import hash_password
from app.database.session import SessionLocal
from app.models.admin_user import AdminUser


def main():
    email = input(
        "Admin email: "
    ).strip().lower()

    password = getpass(
        "Password: "
    )

    confirm_password = getpass(
        "Confirm password: "
    )

    if password != confirm_password:
        print(
            "Passwords do not match."
        )
        return

    if len(password) < 12:
        print(
            "Password must contain at least 12 characters."
        )
        return

    with SessionLocal() as db:
        existing_admin = db.scalar(
            select(AdminUser).where(
                AdminUser.email == email
            )
        )

        if existing_admin is not None:
            print(
                "An admin with that email already exists."
            )
            return

        admin_user = AdminUser(
            email=email,
            password_hash=hash_password(
                password
            ),
            is_active=True,
        )

        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        print(
            f"Admin created successfully with ID {admin_user.id}."
        )


if __name__ == "__main__":
    main()