from sqlalchemy import (
    select,
)
from sqlalchemy.orm import Session

from app.models.media_asset import (
    MediaAsset,
)
from app.models.profile import (
    Profile,
)
from app.models.profile_document import (
    ProfileDocument,
)
from app.models.profile_media import (
    ProfileMedia,
)
from app.models.project import (
    Project,
)
from app.models.project_media import (
    ProjectMedia,
)


class PublicMediaRepository:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    # =====================================================
    # PROFILE
    # =====================================================

    def get_profile(
        self,
    ):
        statement = (
            select(Profile)
            .order_by(
                Profile.id.asc()
            )
            .limit(1)
        )

        return self.db.scalars(
            statement
        ).first()

    def get_profile_media(
        self,
        profile_id: int,
    ):
        statement = (
            select(
                ProfileMedia,
                MediaAsset,
            )
            .join(
                MediaAsset,
                MediaAsset.id
                == ProfileMedia.media_asset_id,
            )
            .where(
                ProfileMedia.profile_id
                == profile_id
            )
            .order_by(
                ProfileMedia.display_order.asc(),
                ProfileMedia.id.asc(),
            )
        )

        return list(
            self.db.execute(
                statement
            ).all()
        )

    # =====================================================
    # DOCUMENTS
    # =====================================================

    def get_profile_documents(
        self,
        profile_id: int,
    ):
        statement = (
            select(
                ProfileDocument,
                MediaAsset,
            )
            .join(
                MediaAsset,
                MediaAsset.id
                == ProfileDocument.media_asset_id,
            )
            .where(
                ProfileDocument.profile_id
                == profile_id,
                ProfileDocument.is_current
                .is_(True),
            )
            .order_by(
                ProfileDocument.id.asc()
            )
        )

        return list(
            self.db.execute(
                statement
            ).all()
        )

    # =====================================================
    # PROJECT
    # =====================================================

    def get_public_project_by_slug(
        self,
        slug: str,
    ):
        statement = (
            select(Project)
            .where(
                Project.slug == slug,
                Project.status
                == "PUBLISHED",
            )
        )

        return self.db.scalars(
            statement
        ).first()

    def get_project_media(
        self,
        project_id: int,
    ):
        statement = (
            select(
                ProjectMedia,
                MediaAsset,
            )
            .join(
                MediaAsset,
                MediaAsset.id
                == ProjectMedia.media_asset_id,
            )
            .where(
                ProjectMedia.project_id
                == project_id,
                ProjectMedia.is_visible
                .is_(True),
            )
            .order_by(
                ProjectMedia.display_order.asc(),
                ProjectMedia.id.asc(),
            )
        )

        return list(
            self.db.execute(
                statement
            ).all()
        )