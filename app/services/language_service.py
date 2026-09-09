from app.core.exceptions import (
    DomainValidationError,
    ResourceConflictError,
    ResourceInUseError,
    ResourceNotFoundError,
)
from app.models.language import Language
from app.models.profile_language import (
    ProfileLanguage,
)
from app.models.proficiency_level import (
    ProficiencyLevel,
)
from app.repositories.language_repository import (
    LanguageRepository,
)
from app.schemas.language import (
    LanguageCreate,
    LanguageUpdate,
    ProfileLanguageCreate,
    ProfileLanguageUpdate,
    ProficiencyLevelCreate,
    ProficiencyLevelUpdate,
)


class LanguageService:
    def __init__(
        self,
        repository: LanguageRepository,
    ):
        self.repository = repository

    def _profile(self):
        profile = self.repository.get_profile()

        if profile is None:
            raise ResourceNotFoundError(
                "Profile has not been created yet"
            )

        return profile

    # LANGUAGES

    def get_languages(self):
        return self.repository.get_languages()

    def create_language(
        self,
        data: LanguageCreate,
    ):
        name = data.name.strip()
        code = data.iso_code.strip().lower()

        if self.repository.get_language_by_name(
            name
        ):
            raise ResourceConflictError(
                "Language already exists"
            )

        if self.repository.get_language_by_code(
            code
        ):
            raise ResourceConflictError(
                "Language ISO code already exists"
            )

        return self.repository.save_language(
            Language(
                name=name,
                iso_code=code,
            )
        )

    def update_language(
        self,
        language_id: int,
        data: LanguageUpdate,
    ):
        language = (
            self.repository.get_language(
                language_id
            )
        )

        if language is None:
            raise ResourceNotFoundError(
                "Language not found"
            )

        changes = data.model_dump(
            exclude_unset=True
        )

        if "name" in changes:
            if changes["name"] is None:
                raise DomainValidationError(
                    "Language name cannot be null"
                )

            name = changes["name"].strip()

            existing = (
                self.repository
                .get_language_by_name(name)
            )

            if (
                existing is not None
                and existing.id != language.id
            ):
                raise ResourceConflictError(
                    "Language already exists"
                )

            language.name = name

        if "iso_code" in changes:
            if changes["iso_code"] is None:
                raise DomainValidationError(
                    "ISO code cannot be null"
                )

            code = (
                changes["iso_code"]
                .strip()
                .lower()
            )

            existing = (
                self.repository
                .get_language_by_code(code)
            )

            if (
                existing is not None
                and existing.id != language.id
            ):
                raise ResourceConflictError(
                    "Language ISO code already exists"
                )

            language.iso_code = code

        return self.repository.save_language(
            language
        )

    def delete_language(
        self,
        language_id: int,
    ):
        language = (
            self.repository.get_language(
                language_id
            )
        )

        if language is None:
            raise ResourceNotFoundError(
                "Language not found"
            )

        if (
            self.repository
            .count_language_usage(language_id)
            > 0
        ):
            raise ResourceInUseError(
                "Language is currently in use"
            )

        self.repository.delete_language(
            language
        )

    # LEVELS

    def get_levels(self):
        return self.repository.get_levels()

    def create_level(
        self,
        data: ProficiencyLevelCreate,
    ):
        code = data.code.strip().upper()

        if self.repository.get_level_by_code(
            code
        ):
            raise ResourceConflictError(
                "Proficiency code already exists"
            )

        if self.repository.get_level_by_rank(
            data.rank
        ):
            raise ResourceConflictError(
                "Proficiency rank already exists"
            )

        return self.repository.save_level(
            ProficiencyLevel(
                code=code,
                name=data.name.strip(),
                rank=data.rank,
            )
        )

    def update_level(
        self,
        level_id: int,
        data: ProficiencyLevelUpdate,
    ):
        level = self.repository.get_level(
            level_id
        )

        if level is None:
            raise ResourceNotFoundError(
                "Proficiency level not found"
            )

        changes = data.model_dump(
            exclude_unset=True
        )

        if "code" in changes:
            if changes["code"] is None:
                raise DomainValidationError(
                    "Code cannot be null"
                )

            code = (
                changes["code"]
                .strip()
                .upper()
            )

            existing = (
                self.repository
                .get_level_by_code(code)
            )

            if (
                existing is not None
                and existing.id != level.id
            ):
                raise ResourceConflictError(
                    "Proficiency code already exists"
                )

            level.code = code

        if "rank" in changes:
            if changes["rank"] is None:
                raise DomainValidationError(
                    "Rank cannot be null"
                )

            existing = (
                self.repository
                .get_level_by_rank(
                    changes["rank"]
                )
            )

            if (
                existing is not None
                and existing.id != level.id
            ):
                raise ResourceConflictError(
                    "Proficiency rank already exists"
                )

            level.rank = changes["rank"]

        if "name" in changes:
            if changes["name"] is None:
                raise DomainValidationError(
                    "Name cannot be null"
                )

            level.name = (
                changes["name"].strip()
            )

        return self.repository.save_level(
            level
        )

    def delete_level(
        self,
        level_id: int,
    ):
        level = self.repository.get_level(
            level_id
        )

        if level is None:
            raise ResourceNotFoundError(
                "Proficiency level not found"
            )

        if (
            self.repository.count_level_usage(
                level_id
            )
            > 0
        ):
            raise ResourceInUseError(
                "Proficiency level is currently in use"
            )

        self.repository.delete_level(
            level
        )

    # PROFILE LANGUAGES

    def get_profile_languages(self):
        profile = self._profile()

        items = (
            self.repository
            .get_profile_languages(
                profile.id
            )
        )

        return items, len(items)

    def add_profile_language(
        self,
        data: ProfileLanguageCreate,
    ):
        profile = self._profile()

        if (
            self.repository.get_language(
                data.language_id
            )
            is None
        ):
            raise ResourceNotFoundError(
                "Language not found"
            )

        if (
            self.repository.get_level(
                data.proficiency_level_id
            )
            is None
        ):
            raise ResourceNotFoundError(
                "Proficiency level not found"
            )

        if (
            self.repository
            .get_profile_language(
                profile.id,
                data.language_id,
            )
            is not None
        ):
            raise ResourceConflictError(
                "Language is already assigned to profile"
            )

        association = ProfileLanguage(
            profile_id=profile.id,
            language_id=data.language_id,
            proficiency_level_id=(
                data.proficiency_level_id
            ),
            display_order=(
                data.display_order
            ),
        )

        return (
            self.repository
            .save_profile_language(
                association
            )
        )

    def update_profile_language(
        self,
        language_id: int,
        data: ProfileLanguageUpdate,
    ):
        profile = self._profile()

        association = (
            self.repository
            .get_profile_language(
                profile.id,
                language_id,
            )
        )

        if association is None:
            raise ResourceNotFoundError(
                "Profile language not found"
            )

        changes = data.model_dump(
            exclude_unset=True
        )

        if "proficiency_level_id" in changes:
            level_id = changes[
                "proficiency_level_id"
            ]

            if level_id is None:
                raise DomainValidationError(
                    "Proficiency level cannot be null"
                )

            if (
                self.repository.get_level(
                    level_id
                )
                is None
            ):
                raise ResourceNotFoundError(
                    "Proficiency level not found"
                )

            association.proficiency_level_id = (
                level_id
            )

        if "display_order" in changes:
            if changes["display_order"] is None:
                raise DomainValidationError(
                    "Display order cannot be null"
                )

            association.display_order = (
                changes["display_order"]
            )

        return (
            self.repository
            .save_profile_language(
                association
            )
        )

    def delete_profile_language(
        self,
        language_id: int,
    ):
        profile = self._profile()

        association = (
            self.repository
            .get_profile_language(
                profile.id,
                language_id,
            )
        )

        if association is None:
            raise ResourceNotFoundError(
                "Profile language not found"
            )

        self.repository.delete_profile_language(
            association
        )