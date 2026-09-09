from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.education import Education
from app.models.experience import Experience
from app.models.media_asset import MediaAsset
from app.models.organization import Organization
from app.models.project import Project


class OrganizationRepository:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def get_all(
        self,
    ) -> list[Organization]:
        statement = (
            select(Organization)
            .order_by(
                Organization.name.asc()
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def count_all(
        self,
    ) -> int:
        statement = select(
            func.count(Organization.id)
        )

        return self.db.scalar(statement) or 0

    def get_by_id(
        self,
        organization_id: int,
    ) -> Organization | None:
        return self.db.get(
            Organization,
            organization_id,
        )

    def get_by_slug(
        self,
        slug: str,
    ) -> Organization | None:
        statement = select(
            Organization
        ).where(
            Organization.slug == slug
        )

        return self.db.scalar(statement)

    def get_by_name(
        self,
        name: str,
    ) -> Organization | None:
        statement = select(
            Organization
        ).where(
            func.lower(Organization.name)
            == name.lower()
        )

        return self.db.scalar(statement)

    def get_media_asset_by_id(
        self,
        media_asset_id: int,
    ) -> MediaAsset | None:
        return self.db.get(
            MediaAsset,
            media_asset_id,
        )

    def create(
        self,
        organization: Organization,
    ) -> Organization:
        self.db.add(organization)
        self.db.commit()
        self.db.refresh(organization)

        return organization

    def update(
        self,
        organization: Organization,
    ) -> Organization:
        self.db.add(organization)
        self.db.commit()
        self.db.refresh(organization)

        return organization

    def delete(
        self,
        organization: Organization,
    ) -> None:
        self.db.delete(organization)
        self.db.commit()

    def count_usage(
        self,
        organization_id: int,
    ) -> int:
        experience_count = (
            self.db.scalar(
                select(func.count())
                .select_from(Experience)
                .where(
                    Experience.organization_id
                    == organization_id
                )
            )
            or 0
        )

        education_count = (
            self.db.scalar(
                select(func.count())
                .select_from(Education)
                .where(
                    Education.organization_id
                    == organization_id
                )
            )
            or 0
        )

        project_count = (
            self.db.scalar(
                select(func.count())
                .select_from(Project)
                .where(
                    Project.organization_id
                    == organization_id
                )
            )
            or 0
        )

        return (
            experience_count
            + education_count
            + project_count
        )