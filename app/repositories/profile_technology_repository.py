from sqlalchemy import select
from sqlalchemy.orm import (
    Session,
    selectinload,
)

from app.models.profile import Profile
from app.models.profile_technology import (
    ProfileTechnology,
)
from app.models.technology import Technology


class ProfileTechnologyRepository:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def get_profile(self):
        return self.db.scalar(
            select(Profile)
            .order_by(Profile.id.asc())
            .limit(1)
        )

    def get_technology(
        self,
        technology_id: int,
    ):
        return self.db.get(
            Technology,
            technology_id,
        )

    def get_all(
        self,
        profile_id: int,
        public_only: bool = False,
    ):
        statement = (
            select(ProfileTechnology)
            .options(
                selectinload(
                    ProfileTechnology.technology
                ).selectinload(
                    Technology.category
                )
            )
            .where(
                ProfileTechnology.profile_id
                == profile_id
            )
        )

        if public_only:
            statement = statement.where(
                ProfileTechnology.is_visible.is_(
                    True
                )
            )

        statement = statement.order_by(
            ProfileTechnology.featured.desc(),
            ProfileTechnology.display_order.asc(),
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get(
        self,
        profile_id: int,
        technology_id: int,
    ):
        statement = (
            select(ProfileTechnology)
            .options(
                selectinload(
                    ProfileTechnology.technology
                ).selectinload(
                    Technology.category
                )
            )
            .where(
                ProfileTechnology.profile_id
                == profile_id,
                ProfileTechnology.technology_id
                == technology_id,
            )
        )

        return self.db.scalar(statement)

    def save(
        self,
        item: ProfileTechnology,
    ):
        self.db.add(item)
        self.db.commit()

        return self.get(
            item.profile_id,
            item.technology_id,
        )

    def delete(
        self,
        item: ProfileTechnology,
    ):
        self.db.delete(item)
        self.db.commit()