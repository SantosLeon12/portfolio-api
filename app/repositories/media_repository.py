from sqlalchemy import (
    func,
    select,
    update,
)
from sqlalchemy.orm import (
    Session,
    selectinload,
)

from app.models.media_asset import MediaAsset
from app.models.organization import Organization
from app.models.profile import Profile
from app.models.profile_document import ProfileDocument
from app.models.profile_media import ProfileMedia
from app.models.project_media import ProjectMedia
from app.models.technology import Technology


class MediaRepository:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    # =====================================================
    # MEDIA ASSETS
    # =====================================================

    def get_all(
        self,
    ) -> list[MediaAsset]:
        statement = (
            select(MediaAsset)
            .order_by(
                MediaAsset.created_at.desc()
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def count_all(
        self,
    ) -> int:
        return (
            self.db.scalar(
                select(
                    func.count(
                        MediaAsset.id
                    )
                )
            )
            or 0
        )

    def get_asset(
        self,
        media_asset_id: int,
    ) -> MediaAsset | None:
        return self.db.get(
            MediaAsset,
            media_asset_id,
        )

    def save_asset(
        self,
        asset: MediaAsset,
    ) -> MediaAsset:
        self.db.add(asset)
        self.db.commit()
        self.db.refresh(asset)

        return asset

    def delete_asset(
        self,
        asset: MediaAsset,
    ) -> None:
        self.db.delete(asset)
        self.db.commit()

    def count_asset_usage(
        self,
        media_asset_id: int,
    ) -> int:

        profile_media = (
            self.db.scalar(
                select(func.count())
                .select_from(ProfileMedia)
                .where(
                    ProfileMedia.media_asset_id
                    == media_asset_id
                )
            )
            or 0
        )

        documents = (
            self.db.scalar(
                select(func.count())
                .select_from(ProfileDocument)
                .where(
                    ProfileDocument.media_asset_id
                    == media_asset_id
                )
            )
            or 0
        )

        organization_logos = (
            self.db.scalar(
                select(func.count())
                .select_from(Organization)
                .where(
                    Organization.logo_media_id
                    == media_asset_id
                )
            )
            or 0
        )

        technology_icons = (
            self.db.scalar(
                select(func.count())
                .select_from(Technology)
                .where(
                    Technology.icon_media_id
                    == media_asset_id
                )
            )
            or 0
        )

        project_media = (
            self.db.scalar(
                select(func.count())
                .select_from(ProjectMedia)
                .where(
                    ProjectMedia.media_asset_id
                    == media_asset_id
                )
            )
            or 0
        )

        return (
            profile_media
            + documents
            + organization_logos
            + technology_icons
            + project_media
        )

    # =====================================================
    # PROFILE
    # =====================================================

    def get_profile(
        self,
    ) -> Profile | None:
        return self.db.scalar(
            select(Profile)
            .order_by(Profile.id.asc())
            .limit(1)
        )

    # =====================================================
    # PROFILE MEDIA
    # =====================================================

    def get_all_profile_media(
        self,
        profile_id: int,
    ) -> list[ProfileMedia]:
        statement = (
            select(ProfileMedia)
            .options(
                selectinload(
                    ProfileMedia.media_asset
                )
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
            self.db.scalars(
                statement
            ).all()
        )

    def get_profile_media(
        self,
        profile_media_id: int,
    ) -> ProfileMedia | None:
        statement = (
            select(ProfileMedia)
            .options(
                selectinload(
                    ProfileMedia.media_asset
                )
            )
            .where(
                ProfileMedia.id
                == profile_media_id
            )
        )

        return self.db.scalar(statement)

    def get_profile_media_by_asset(
        self,
        profile_id: int,
        media_asset_id: int,
    ) -> ProfileMedia | None:
        return self.db.scalar(
            select(ProfileMedia).where(
                ProfileMedia.profile_id
                == profile_id,
                ProfileMedia.media_asset_id
                == media_asset_id,
            )
        )

    def save_profile_media(
        self,
        profile_media: ProfileMedia,
    ) -> ProfileMedia:
        self.db.add(profile_media)
        self.db.commit()

        return self.get_profile_media(
            profile_media.id
        )

    def delete_profile_media(
        self,
        profile_media: ProfileMedia,
    ) -> None:
        self.db.delete(profile_media)
        self.db.commit()

    # =====================================================
    # PROFILE DOCUMENTS
    # =====================================================

    def get_all_documents(
        self,
        profile_id: int,
    ) -> list[ProfileDocument]:
        statement = (
            select(ProfileDocument)
            .options(
                selectinload(
                    ProfileDocument.media_asset
                )
            )
            .where(
                ProfileDocument.profile_id
                == profile_id
            )
            .order_by(
                ProfileDocument.document_type.asc(),
                ProfileDocument.is_current.desc(),
                ProfileDocument.id.desc(),
            )
        )

        return list(
            self.db.scalars(
                statement
            ).all()
        )

    def get_document(
        self,
        document_id: int,
    ) -> ProfileDocument | None:
        statement = (
            select(ProfileDocument)
            .options(
                selectinload(
                    ProfileDocument.media_asset
                )
            )
            .where(
                ProfileDocument.id
                == document_id
            )
        )

        return self.db.scalar(statement)

    def get_document_by_asset(
        self,
        profile_id: int,
        media_asset_id: int,
    ) -> ProfileDocument | None:
        return self.db.scalar(
            select(ProfileDocument).where(
                ProfileDocument.profile_id
                == profile_id,
                ProfileDocument.media_asset_id
                == media_asset_id,
            )
        )

    def unset_current_documents(
        self,
        profile_id: int,
        document_type: str,
        exclude_document_id: int | None = None,
    ) -> None:

        statement = (
            update(ProfileDocument)
            .where(
                ProfileDocument.profile_id
                == profile_id,
                ProfileDocument.document_type
                == document_type,
                ProfileDocument.is_current.is_(
                    True
                ),
            )
            .values(
                is_current=False
            )
        )

        if exclude_document_id is not None:
            statement = statement.where(
                ProfileDocument.id
                != exclude_document_id
            )

        self.db.execute(statement)

    def save_document(
        self,
        document: ProfileDocument,
    ) -> ProfileDocument:
        self.db.add(document)
        self.db.commit()

        return self.get_document(
            document.id
        )

    def delete_document(
        self,
        document: ProfileDocument,
    ) -> None:
        self.db.delete(document)
        self.db.commit()