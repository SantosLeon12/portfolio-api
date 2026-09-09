from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.experience_technology import (
    ExperienceTechnology,
)
from app.models.media_asset import MediaAsset
from app.models.profile_technology import (
    ProfileTechnology,
)
from app.models.project_technology import (
    ProjectTechnology,
)
from app.models.technology import Technology
from app.models.technology_category import (
    TechnologyCategory,
)


class TechnologyRepository:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    # -------------------------
    # TECHNOLOGY READ
    # -------------------------

    def get_all(
        self,
    ) -> list[Technology]:
        statement = (
            select(Technology)
            .options(
                selectinload(
                    Technology.category
                ),
            )
            .order_by(
                Technology.name.asc(),
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def count_all(self) -> int:
        statement = select(
            func.count(Technology.id)
        )

        return self.db.scalar(statement) or 0

    def get_by_id(
        self,
        technology_id: int,
    ) -> Technology | None:
        statement = (
            select(Technology)
            .options(
                selectinload(
                    Technology.category
                ),
            )
            .where(
                Technology.id == technology_id
            )
        )

        return self.db.scalar(statement)

    def get_by_slug(
        self,
        slug: str,
    ) -> Technology | None:
        statement = (
            select(Technology)
            .options(
                selectinload(
                    Technology.category
                ),
            )
            .where(
                Technology.slug == slug
            )
        )

        return self.db.scalar(statement)

    def get_by_name(
        self,
        name: str,
    ) -> Technology | None:
        statement = select(
            Technology
        ).where(
            func.lower(Technology.name)
            == name.lower()
        )

        return self.db.scalar(statement)

    # -------------------------
    # CATEGORY READ
    # -------------------------

    def get_category_by_id(
        self,
        category_id: int,
    ) -> TechnologyCategory | None:
        return self.db.get(
            TechnologyCategory,
            category_id,
        )

    def get_category_by_slug(
        self,
        slug: str,
    ) -> TechnologyCategory | None:
        statement = select(
            TechnologyCategory
        ).where(
            TechnologyCategory.slug == slug
        )

        return self.db.scalar(statement)

    def get_category_by_name(
        self,
        name: str,
    ) -> TechnologyCategory | None:
        statement = select(
            TechnologyCategory
        ).where(
            func.lower(
                TechnologyCategory.name
            )
            == name.lower()
        )

        return self.db.scalar(statement)

    def get_categories(
        self,
    ) -> list[TechnologyCategory]:
        statement = select(
            TechnologyCategory
        ).order_by(
            TechnologyCategory.display_order.asc(),
            TechnologyCategory.name.asc(),
        )

        return list(
            self.db.scalars(statement).all()
        )

    # -------------------------
    # MEDIA
    # -------------------------

    def get_media_asset_by_id(
        self,
        media_asset_id: int,
    ) -> MediaAsset | None:
        return self.db.get(
            MediaAsset,
            media_asset_id,
        )

    # -------------------------
    # TECHNOLOGY WRITE
    # -------------------------

    def create_technology(
        self,
        technology: Technology,
    ) -> Technology:
        self.db.add(technology)
        self.db.commit()
        self.db.refresh(technology)

        return self.get_by_id(
            technology.id
        )

    def update_technology(
        self,
        technology: Technology,
    ) -> Technology:
        self.db.add(technology)
        self.db.commit()
        self.db.refresh(technology)

        return self.get_by_id(
            technology.id
        )

    def delete_technology(
        self,
        technology: Technology,
    ) -> None:
        self.db.delete(technology)
        self.db.commit()

    # -------------------------
    # CATEGORY WRITE
    # -------------------------

    def create_category(
        self,
        category: TechnologyCategory,
    ) -> TechnologyCategory:
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)

        return category

    def update_category(
        self,
        category: TechnologyCategory,
    ) -> TechnologyCategory:
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)

        return category

    def delete_category(
        self,
        category: TechnologyCategory,
    ) -> None:
        self.db.delete(category)
        self.db.commit()

    # -------------------------
    # USAGE CHECKS
    # -------------------------

    def count_technologies_by_category(
        self,
        category_id: int,
    ) -> int:
        statement = select(
            func.count(Technology.id)
        ).where(
            Technology.technology_category_id
            == category_id
        )

        return self.db.scalar(statement) or 0

    def count_technology_usage(
        self,
        technology_id: int,
    ) -> int:
        profile_count = (
            self.db.scalar(
                select(
                    func.count()
                ).select_from(
                    ProfileTechnology
                ).where(
                    ProfileTechnology.technology_id
                    == technology_id
                )
            )
            or 0
        )

        experience_count = (
            self.db.scalar(
                select(
                    func.count()
                ).select_from(
                    ExperienceTechnology
                ).where(
                    ExperienceTechnology.technology_id
                    == technology_id
                )
            )
            or 0
        )

        project_count = (
            self.db.scalar(
                select(
                    func.count()
                ).select_from(
                    ProjectTechnology
                ).where(
                    ProjectTechnology.technology_id
                    == technology_id
                )
            )
            or 0
        )

        return (
            profile_count
            + experience_count
            + project_count
        )