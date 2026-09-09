from app.core.exceptions import (
    DomainValidationError,
    ResourceConflictError,
    ResourceInUseError,
    ResourceNotFoundError,
)
from app.models.technology import Technology
from app.models.technology_category import (
    TechnologyCategory,
)
from app.repositories.technology_repository import (
    TechnologyRepository,
)
from app.schemas.technology import (
    TechnologyCategoryCreate,
    TechnologyCategoryUpdate,
    TechnologyCreate,
    TechnologyUpdate,
)


class TechnologyService:
    def __init__(
        self,
        repository: TechnologyRepository,
    ):
        self.repository = repository

    # -------------------------
    # PUBLIC READ
    # -------------------------

    def get_all(
        self,
    ) -> tuple[list[Technology], int]:
        technologies = (
            self.repository.get_all()
        )

        total = (
            self.repository.count_all()
        )

        return technologies, total

    def get_by_slug(
        self,
        slug: str,
    ) -> Technology | None:
        return self.repository.get_by_slug(
            slug=slug,
        )

    def get_categories(
        self,
    ) -> list[TechnologyCategory]:
        return (
            self.repository.get_categories()
        )

    # -------------------------
    # CATEGORY CREATE
    # -------------------------

    def create_category(
        self,
        data: TechnologyCategoryCreate,
    ) -> TechnologyCategory:
        name = data.name.strip()
        slug = data.slug.strip().lower()

        if self.repository.get_category_by_name(
            name
        ):
            raise ResourceConflictError(
                "A technology category with that name already exists"
            )

        if self.repository.get_category_by_slug(
            slug
        ):
            raise ResourceConflictError(
                "A technology category with that slug already exists"
            )

        category = TechnologyCategory(
            name=name,
            slug=slug,
            display_order=data.display_order,
        )

        return self.repository.create_category(
            category
        )

    # -------------------------
    # CATEGORY UPDATE
    # -------------------------

    def update_category(
        self,
        category_id: int,
        data: TechnologyCategoryUpdate,
    ) -> TechnologyCategory:
        category = (
            self.repository.get_category_by_id(
                category_id
            )
        )

        if category is None:
            raise ResourceNotFoundError(
                "Technology category not found"
            )

        changes = data.model_dump(
            exclude_unset=True
        )

        if "name" in changes:
            if changes["name"] is None:
                raise DomainValidationError(
                    "Category name cannot be null"
                )

            name = changes["name"].strip()

            existing = (
                self.repository
                .get_category_by_name(name)
            )

            if (
                existing is not None
                and existing.id != category.id
            ):
                raise ResourceConflictError(
                    "A technology category with that name already exists"
                )

            category.name = name

        if "slug" in changes:
            if changes["slug"] is None:
                raise DomainValidationError(
                    "Category slug cannot be null"
                )

            slug = (
                changes["slug"]
                .strip()
                .lower()
            )

            existing = (
                self.repository
                .get_category_by_slug(slug)
            )

            if (
                existing is not None
                and existing.id != category.id
            ):
                raise ResourceConflictError(
                    "A technology category with that slug already exists"
                )

            category.slug = slug

        if "display_order" in changes:
            if (
                changes["display_order"]
                is None
            ):
                raise DomainValidationError(
                    "Display order cannot be null"
                )

            category.display_order = (
                changes["display_order"]
            )

        return (
            self.repository.update_category(
                category
            )
        )

    # -------------------------
    # CATEGORY DELETE
    # -------------------------

    def delete_category(
        self,
        category_id: int,
    ) -> None:
        category = (
            self.repository.get_category_by_id(
                category_id
            )
        )

        if category is None:
            raise ResourceNotFoundError(
                "Technology category not found"
            )

        usage = (
            self.repository
            .count_technologies_by_category(
                category_id
            )
        )

        if usage > 0:
            raise ResourceInUseError(
                "Technology category cannot be deleted because it contains technologies"
            )

        self.repository.delete_category(
            category
        )

    # -------------------------
    # TECHNOLOGY CREATE
    # -------------------------

    def create_technology(
        self,
        data: TechnologyCreate,
    ) -> Technology:
        name = data.name.strip()
        slug = data.slug.strip().lower()

        if self.repository.get_by_name(name):
            raise ResourceConflictError(
                "A technology with that name already exists"
            )

        if self.repository.get_by_slug(slug):
            raise ResourceConflictError(
                "A technology with that slug already exists"
            )

        category = (
            self.repository
            .get_category_by_id(
                data.technology_category_id
            )
        )

        if category is None:
            raise ResourceNotFoundError(
                "Technology category not found"
            )

        if data.icon_media_id is not None:
            media = (
                self.repository
                .get_media_asset_by_id(
                    data.icon_media_id
                )
            )

            if media is None:
                raise ResourceNotFoundError(
                    "Media asset not found"
                )

        technology = Technology(
            technology_category_id=(
                data.technology_category_id
            ),
            name=name,
            slug=slug,
            official_url=data.official_url,
            icon_media_id=(
                data.icon_media_id
            ),
        )

        return (
            self.repository
            .create_technology(
                technology
            )
        )

    # -------------------------
    # TECHNOLOGY UPDATE
    # -------------------------

    def update_technology(
        self,
        technology_id: int,
        data: TechnologyUpdate,
    ) -> Technology:
        technology = (
            self.repository.get_by_id(
                technology_id
            )
        )

        if technology is None:
            raise ResourceNotFoundError(
                "Technology not found"
            )

        changes = data.model_dump(
            exclude_unset=True
        )

        if "name" in changes:
            if changes["name"] is None:
                raise DomainValidationError(
                    "Technology name cannot be null"
                )

            name = changes["name"].strip()

            existing = (
                self.repository
                .get_by_name(name)
            )

            if (
                existing is not None
                and existing.id
                != technology.id
            ):
                raise ResourceConflictError(
                    "A technology with that name already exists"
                )

            technology.name = name

        if "slug" in changes:
            if changes["slug"] is None:
                raise DomainValidationError(
                    "Technology slug cannot be null"
                )

            slug = (
                changes["slug"]
                .strip()
                .lower()
            )

            existing = (
                self.repository
                .get_by_slug(slug)
            )

            if (
                existing is not None
                and existing.id
                != technology.id
            ):
                raise ResourceConflictError(
                    "A technology with that slug already exists"
                )

            technology.slug = slug

        if (
            "technology_category_id"
            in changes
        ):
            category_id = changes[
                "technology_category_id"
            ]

            if category_id is None:
                raise DomainValidationError(
                    "Technology category cannot be null"
                )

            category = (
                self.repository
                .get_category_by_id(
                    category_id
                )
            )

            if category is None:
                raise ResourceNotFoundError(
                    "Technology category not found"
                )

            technology.technology_category_id = (
                category_id
            )

        if "icon_media_id" in changes:
            icon_media_id = changes[
                "icon_media_id"
            ]

            if icon_media_id is not None:
                media = (
                    self.repository
                    .get_media_asset_by_id(
                        icon_media_id
                    )
                )

                if media is None:
                    raise ResourceNotFoundError(
                        "Media asset not found"
                    )

            technology.icon_media_id = (
                icon_media_id
            )

        if "official_url" in changes:
            technology.official_url = (
                changes["official_url"]
            )

        return (
            self.repository
            .update_technology(
                technology
            )
        )

    # -------------------------
    # TECHNOLOGY DELETE
    # -------------------------

    def delete_technology(
        self,
        technology_id: int,
    ) -> None:
        technology = (
            self.repository.get_by_id(
                technology_id
            )
        )

        if technology is None:
            raise ResourceNotFoundError(
                "Technology not found"
            )

        usage = (
            self.repository
            .count_technology_usage(
                technology_id
            )
        )

        if usage > 0:
            raise ResourceInUseError(
                "Technology cannot be deleted because it is currently associated with the portfolio"
            )

        self.repository.delete_technology(
            technology
        )