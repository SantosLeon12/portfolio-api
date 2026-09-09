from app.core.exceptions import (
    DomainValidationError,
    ResourceConflictError,
    ResourceNotFoundError,
)
from app.models.profile_technology import (
    ProfileTechnology,
)
from app.repositories.profile_technology_repository import (
    ProfileTechnologyRepository,
)
from app.schemas.technology import (
    ProfileTechnologyCreate,
    ProfileTechnologyUpdate,
)


class ProfileTechnologyService:
    def __init__(
        self,
        repository: ProfileTechnologyRepository,
    ):
        self.repository = repository

    def _profile(self):
        profile = self.repository.get_profile()

        if profile is None:
            raise ResourceNotFoundError(
                "Profile has not been created yet"
            )

        return profile

    def get_all(
        self,
        public_only: bool = False,
    ):
        profile = self._profile()

        items = self.repository.get_all(
            profile.id,
            public_only=public_only,
        )

        return items, len(items)

    def create(
        self,
        data: ProfileTechnologyCreate,
    ):
        profile = self._profile()

        if (
            self.repository.get_technology(
                data.technology_id
            )
            is None
        ):
            raise ResourceNotFoundError(
                "Technology not found"
            )

        if (
            self.repository.get(
                profile.id,
                data.technology_id,
            )
            is not None
        ):
            raise ResourceConflictError(
                "Technology is already assigned to profile"
            )

        item = ProfileTechnology(
            profile_id=profile.id,
            technology_id=data.technology_id,
            featured=data.featured,
            display_order=data.display_order,
            is_visible=data.is_visible,
        )

        return self.repository.save(item)

    def update(
        self,
        technology_id: int,
        data: ProfileTechnologyUpdate,
    ):
        profile = self._profile()

        item = self.repository.get(
            profile.id,
            technology_id,
        )

        if item is None:
            raise ResourceNotFoundError(
                "Profile technology not found"
            )

        changes = data.model_dump(
            exclude_unset=True
        )

        for field in (
            "featured",
            "display_order",
            "is_visible",
        ):
            if field in changes:
                if changes[field] is None:
                    raise DomainValidationError(
                        f"{field} cannot be null"
                    )

                setattr(
                    item,
                    field,
                    changes[field],
                )

        return self.repository.save(item)

    def delete(
        self,
        technology_id: int,
    ):
        profile = self._profile()

        item = self.repository.get(
            profile.id,
            technology_id,
        )

        if item is None:
            raise ResourceNotFoundError(
                "Profile technology not found"
            )

        self.repository.delete(item)