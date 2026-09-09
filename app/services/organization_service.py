from app.core.exceptions import (
    DomainValidationError,
    ResourceConflictError,
    ResourceInUseError,
    ResourceNotFoundError,
)
from app.models.organization import Organization
from app.repositories.organization_repository import (
    OrganizationRepository,
)
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationUpdate,
)


class OrganizationService:
    ALLOWED_TYPES = {
        "COMPANY",
        "UNIVERSITY",
        "SCHOOL",
        "CLIENT",
        "OTHER",
    }

    def __init__(
        self,
        repository: OrganizationRepository,
    ):
        self.repository = repository

    def get_all(
        self,
    ) -> tuple[list[Organization], int]:
        organizations = (
            self.repository.get_all()
        )

        total = self.repository.count_all()

        return organizations, total

    def get_by_id(
        self,
        organization_id: int,
    ) -> Organization:
        organization = (
            self.repository.get_by_id(
                organization_id
            )
        )

        if organization is None:
            raise ResourceNotFoundError(
                "Organization not found"
            )

        return organization

    def create(
        self,
        data: OrganizationCreate,
    ) -> Organization:
        name = data.name.strip()
        slug = data.slug.strip().lower()

        organization_type = (
            data.organization_type
            .strip()
            .upper()
        )

        if (
            organization_type
            not in self.ALLOWED_TYPES
        ):
            raise DomainValidationError(
                "Invalid organization type"
            )

        if self.repository.get_by_name(name):
            raise ResourceConflictError(
                "An organization with that name already exists"
            )

        if self.repository.get_by_slug(slug):
            raise ResourceConflictError(
                "An organization with that slug already exists"
            )

        if data.logo_media_id is not None:
            media = (
                self.repository
                .get_media_asset_by_id(
                    data.logo_media_id
                )
            )

            if media is None:
                raise ResourceNotFoundError(
                    "Media asset not found"
                )

        organization = Organization(
            name=name,
            slug=slug,
            organization_type=(
                organization_type
            ),
            website_url=data.website_url,
            logo_media_id=(
                data.logo_media_id
            ),
        )

        return self.repository.create(
            organization
        )

    def update(
        self,
        organization_id: int,
        data: OrganizationUpdate,
    ) -> Organization:
        organization = self.get_by_id(
            organization_id
        )

        changes = data.model_dump(
            exclude_unset=True
        )

        if "name" in changes:
            if changes["name"] is None:
                raise DomainValidationError(
                    "Organization name cannot be null"
                )

            name = changes["name"].strip()

            existing = (
                self.repository.get_by_name(
                    name
                )
            )

            if (
                existing is not None
                and existing.id
                != organization.id
            ):
                raise ResourceConflictError(
                    "An organization with that name already exists"
                )

            organization.name = name

        if "slug" in changes:
            if changes["slug"] is None:
                raise DomainValidationError(
                    "Organization slug cannot be null"
                )

            slug = (
                changes["slug"]
                .strip()
                .lower()
            )

            existing = (
                self.repository.get_by_slug(
                    slug
                )
            )

            if (
                existing is not None
                and existing.id
                != organization.id
            ):
                raise ResourceConflictError(
                    "An organization with that slug already exists"
                )

            organization.slug = slug

        if "organization_type" in changes:
            if (
                changes["organization_type"]
                is None
            ):
                raise DomainValidationError(
                    "Organization type cannot be null"
                )

            organization_type = (
                changes["organization_type"]
                .strip()
                .upper()
            )

            if (
                organization_type
                not in self.ALLOWED_TYPES
            ):
                raise DomainValidationError(
                    "Invalid organization type"
                )

            organization.organization_type = (
                organization_type
            )

        if "logo_media_id" in changes:
            media_id = changes[
                "logo_media_id"
            ]

            if media_id is not None:
                media = (
                    self.repository
                    .get_media_asset_by_id(
                        media_id
                    )
                )

                if media is None:
                    raise ResourceNotFoundError(
                        "Media asset not found"
                    )

            organization.logo_media_id = (
                media_id
            )

        if "website_url" in changes:
            organization.website_url = (
                changes["website_url"]
            )

        return self.repository.update(
            organization
        )

    def delete(
        self,
        organization_id: int,
    ) -> None:
        organization = self.get_by_id(
            organization_id
        )

        usage = self.repository.count_usage(
            organization_id
        )

        if usage > 0:
            raise ResourceInUseError(
                "Organization cannot be deleted because it is currently in use"
            )

        self.repository.delete(
            organization
        )