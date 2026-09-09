from fastapi import UploadFile

from app.core.exceptions import (
    DomainValidationError,
    ResourceConflictError,
    ResourceInUseError,
    ResourceNotFoundError,
)
from app.core.storage import (
    delete_from_cloudinary,
    upload_to_cloudinary,
)
from app.models.media_asset import MediaAsset
from app.models.profile_document import ProfileDocument
from app.models.profile_media import ProfileMedia
from app.repositories.media_repository import (
    MediaRepository,
)
from app.schemas.media import (
    ProfileDocumentCreate,
    ProfileDocumentUpdate,
    ProfileMediaCreate,
    ProfileMediaUpdate,
)


class MediaService:
    MAX_FILE_SIZE = 10 * 1024 * 1024

    ALLOWED_MIME_TYPES = {
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/gif",
        "image/svg+xml",
        "application/pdf",
    }

    PROFILE_MEDIA_ROLES = {
        "AVATAR",
        "HERO",
        "ABOUT",
        "BACKGROUND",
        "OTHER",
    }

    DOCUMENT_TYPES = {
        "CV",
        "RESUME",
        "CERTIFICATE",
        "OTHER",
    }

    def __init__(
        self,
        repository: MediaRepository,
    ):
        self.repository = repository

    def _profile(self):
        profile = self.repository.get_profile()

        if profile is None:
            raise ResourceNotFoundError(
                "Profile has not been created yet"
            )

        return profile

    # =====================================================
    # ASSETS
    # =====================================================

    def get_all(self):
        items = self.repository.get_all()
        total = self.repository.count_all()

        return items, total

    def get_asset(
        self,
        media_asset_id: int,
    ):
        asset = self.repository.get_asset(
            media_asset_id
        )

        if asset is None:
            raise ResourceNotFoundError(
                "Media asset not found"
            )

        return asset

    def upload(
        self,
        file: UploadFile,
    ):
        mime_type = (
            file.content_type
            or "application/octet-stream"
        )

        if (
            mime_type
            not in self.ALLOWED_MIME_TYPES
        ):
            raise DomainValidationError(
                "Unsupported file type"
            )

        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)

        if file_size > self.MAX_FILE_SIZE:
            raise DomainValidationError(
                "File exceeds the 10 MB limit"
            )

        result = upload_to_cloudinary(
            file=file.file,
            mime_type=mime_type,
        )

        asset = MediaAsset(
            storage_provider="cloudinary",
            storage_key=result["public_id"],
            url=result["secure_url"],
            mime_type=mime_type,
            file_size=file_size,
            width=result.get("width"),
            height=result.get("height"),
        )

        return self.repository.save_asset(
            asset
        )

    def delete_asset(
        self,
        media_asset_id: int,
    ) -> None:
        asset = self.get_asset(
            media_asset_id
        )

        usage = (
            self.repository.count_asset_usage(
                media_asset_id
            )
        )

        if usage > 0:
            raise ResourceInUseError(
                "Media asset cannot be deleted because it is currently in use"
            )

        if (
            asset.storage_provider
            == "cloudinary"
        ):
            delete_from_cloudinary(
                asset.storage_key,
                asset.mime_type
                or "application/octet-stream",
            )

        self.repository.delete_asset(
            asset
        )

    # =====================================================
    # PROFILE MEDIA
    # =====================================================

    def get_profile_media_items(
        self,
    ):
        profile = self._profile()

        return (
            self.repository
            .get_all_profile_media(
                profile.id
            )
        )

    def create_profile_media(
        self,
        data: ProfileMediaCreate,
    ):
        profile = self._profile()

        if (
            self.repository.get_asset(
                data.media_asset_id
            )
            is None
        ):
            raise ResourceNotFoundError(
                "Media asset not found"
            )

        role = data.media_role.strip().upper()

        if role not in self.PROFILE_MEDIA_ROLES:
            raise DomainValidationError(
                "Invalid profile media role"
            )

        existing = (
            self.repository
            .get_profile_media_by_asset(
                profile.id,
                data.media_asset_id,
            )
        )

        if existing is not None:
            raise ResourceConflictError(
                "Media asset is already assigned to profile"
            )

        item = ProfileMedia(
            profile_id=profile.id,
            media_asset_id=(
                data.media_asset_id
            ),
            media_role=role,
            alt_text=data.alt_text,
            display_order=data.display_order,
        )

        return (
            self.repository.save_profile_media(
                item
            )
        )

    def update_profile_media(
        self,
        profile_media_id: int,
        data: ProfileMediaUpdate,
    ):
        profile = self._profile()

        item = (
            self.repository.get_profile_media(
                profile_media_id
            )
        )

        if (
            item is None
            or item.profile_id != profile.id
        ):
            raise ResourceNotFoundError(
                "Profile media not found"
            )

        changes = data.model_dump(
            exclude_unset=True
        )

        if "media_role" in changes:
            if changes["media_role"] is None:
                raise DomainValidationError(
                    "Media role cannot be null"
                )

            role = (
                changes["media_role"]
                .strip()
                .upper()
            )

            if role not in self.PROFILE_MEDIA_ROLES:
                raise DomainValidationError(
                    "Invalid profile media role"
                )

            item.media_role = role

        for field in (
            "alt_text",
            "display_order",
        ):
            if field in changes:
                if (
                    field == "display_order"
                    and changes[field] is None
                ):
                    raise DomainValidationError(
                        "Display order cannot be null"
                    )

                setattr(
                    item,
                    field,
                    changes[field],
                )

        return (
            self.repository.save_profile_media(
                item
            )
        )

    def delete_profile_media(
        self,
        profile_media_id: int,
    ) -> None:
        profile = self._profile()

        item = (
            self.repository.get_profile_media(
                profile_media_id
            )
        )

        if (
            item is None
            or item.profile_id != profile.id
        ):
            raise ResourceNotFoundError(
                "Profile media not found"
            )

        self.repository.delete_profile_media(
            item
        )

    # =====================================================
    # DOCUMENTS
    # =====================================================

    def get_documents(
        self,
    ):
        profile = self._profile()

        return (
            self.repository
            .get_all_documents(
                profile.id
            )
        )

    def create_document(
        self,
        data: ProfileDocumentCreate,
    ):
        profile = self._profile()

        if (
            self.repository.get_asset(
                data.media_asset_id
            )
            is None
        ):
            raise ResourceNotFoundError(
                "Media asset not found"
            )

        document_type = (
            data.document_type
            .strip()
            .upper()
        )

        if (
            document_type
            not in self.DOCUMENT_TYPES
        ):
            raise DomainValidationError(
                "Invalid document type"
            )

        existing = (
            self.repository
            .get_document_by_asset(
                profile.id,
                data.media_asset_id,
            )
        )

        if existing is not None:
            raise ResourceConflictError(
                "Media asset is already assigned as a profile document"
            )

        if data.is_current:
            self.repository.unset_current_documents(
                profile.id,
                document_type,
            )

        document = ProfileDocument(
            profile_id=profile.id,
            media_asset_id=(
                data.media_asset_id
            ),
            document_type=document_type,
            title=data.title.strip(),
            version=data.version,
            is_current=data.is_current,
        )

        return (
            self.repository.save_document(
                document
            )
        )

    def update_document(
        self,
        document_id: int,
        data: ProfileDocumentUpdate,
    ):
        profile = self._profile()

        document = (
            self.repository.get_document(
                document_id
            )
        )

        if (
            document is None
            or document.profile_id
            != profile.id
        ):
            raise ResourceNotFoundError(
                "Profile document not found"
            )

        changes = data.model_dump(
            exclude_unset=True
        )

        if "document_type" in changes:
            if changes["document_type"] is None:
                raise DomainValidationError(
                    "Document type cannot be null"
                )

            document_type = (
                changes["document_type"]
                .strip()
                .upper()
            )

            if (
                document_type
                not in self.DOCUMENT_TYPES
            ):
                raise DomainValidationError(
                    "Invalid document type"
                )

            document.document_type = (
                document_type
            )

        if "title" in changes:
            if changes["title"] is None:
                raise DomainValidationError(
                    "Document title cannot be null"
                )

            document.title = (
                changes["title"].strip()
            )

        if "version" in changes:
            document.version = (
                changes["version"]
            )

        if "is_current" in changes:
            if changes["is_current"] is None:
                raise DomainValidationError(
                    "is_current cannot be null"
                )

            document.is_current = (
                changes["is_current"]
            )

        if document.is_current:
            self.repository.unset_current_documents(
                profile.id,
                document.document_type,
                exclude_document_id=(
                    document.id
                ),
            )

        return (
            self.repository.save_document(
                document
            )
        )

    def delete_document(
        self,
        document_id: int,
    ) -> None:
        profile = self._profile()

        document = (
            self.repository.get_document(
                document_id
            )
        )

        if (
            document is None
            or document.profile_id
            != profile.id
        ):
            raise ResourceNotFoundError(
                "Profile document not found"
            )

        self.repository.delete_document(
            document
        )