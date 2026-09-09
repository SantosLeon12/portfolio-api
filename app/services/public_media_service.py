from app.core.exceptions import (
    ResourceNotFoundError,
)
from app.repositories.public_media_repository import (
    PublicMediaRepository,
)


class PublicMediaService:
    def __init__(
        self,
        repository: PublicMediaRepository,
    ):
        self.repository = repository

    # =====================================================
    # INTERNAL
    # =====================================================

    def _get_profile(
        self,
    ):
        profile = (
            self.repository
            .get_profile()
        )

        if profile is None:
            raise ResourceNotFoundError(
                "Profile has not been created yet"
            )

        return profile

    @staticmethod
    def _media_asset_response(
        media_asset,
    ):
        return {
            "id":
                media_asset.id,

            "url":
                media_asset.url,

            "mime_type":
                media_asset.mime_type,

            "width":
                media_asset.width,

            "height":
                media_asset.height,
        }

    # =====================================================
    # PROFILE MEDIA
    # =====================================================

    def get_profile_media(
        self,
    ):
        profile = self._get_profile()

        rows = (
            self.repository
            .get_profile_media(
                profile.id
            )
        )

        return [
            {
                "id":
                    profile_media.id,

                "media_role":
                    profile_media.media_role,

                "alt_text":
                    profile_media.alt_text,

                "display_order":
                    profile_media.display_order,

                "media_asset":
                    self._media_asset_response(
                        media_asset
                    ),
            }
            for (
                profile_media,
                media_asset,
            ) in rows
        ]

    # =====================================================
    # DOCUMENTS
    # =====================================================

    def get_profile_documents(
        self,
    ):
        profile = self._get_profile()

        rows = (
            self.repository
            .get_profile_documents(
                profile.id
            )
        )

        return [
            {
                "id":
                    document.id,

                "document_type":
                    document.document_type,

                "title":
                    document.title,

                "version":
                    document.version,

                "media_asset":
                    self._media_asset_response(
                        media_asset
                    ),
            }
            for (
                document,
                media_asset,
            ) in rows
        ]

    # =====================================================
    # PROJECT MEDIA
    # =====================================================

    def get_project_media(
        self,
        project_slug: str,
    ):
        slug = (
            project_slug
            .strip()
            .lower()
        )

        project = (
            self.repository
            .get_public_project_by_slug(
                slug
            )
        )

        if project is None:
            raise ResourceNotFoundError(
                "Project not found"
            )

        rows = (
            self.repository
            .get_project_media(
                project.id
            )
        )

        return [
            {
                "id":
                    project_media.id,

                "media_role":
                    project_media.media_role,

                "alt_text":
                    project_media.alt_text,

                "caption":
                    project_media.caption,

                "display_order":
                    project_media.display_order,

                "media_asset":
                    self._media_asset_response(
                        media_asset
                    ),
            }
            for (
                project_media,
                media_asset,
            ) in rows
        ]