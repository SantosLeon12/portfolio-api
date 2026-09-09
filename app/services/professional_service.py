from app.core.exceptions import (
    DomainValidationError,
    ResourceConflictError,
    ResourceNotFoundError,
)
from app.models.education import Education
from app.models.experience import Experience
from app.models.experience_highlight import (
    ExperienceHighlight,
)
from app.models.experience_technology import (
    ExperienceTechnology,
)
from app.repositories.professional_repository import (
    ProfessionalRepository,
)
from app.schemas.professional import (
    EducationCreate,
    EducationUpdate,
    ExperienceCreate,
    ExperienceHighlightCreate,
    ExperienceHighlightUpdate,
    ExperienceTechnologyCreate,
    ExperienceTechnologyUpdate,
    ExperienceUpdate,
)


class ProfessionalService:
    def __init__(
        self,
        repository: ProfessionalRepository,
    ):
        self.repository = repository

    def _profile(self):
        profile = self.repository.get_profile()

        if profile is None:
            raise ResourceNotFoundError(
                "Profile has not been created yet"
            )

        return profile

    @staticmethod
    def _validate_dates(
        start_date,
        end_date,
    ):
        if (
            end_date is not None
            and end_date < start_date
        ):
            raise DomainValidationError(
                "End date cannot be earlier than start date"
            )

    # =====================================================
    # EXPERIENCES
    # =====================================================

    def get_experiences(
        self,
        public_only: bool = False,
    ):
        profile = self._profile()

        items = (
            self.repository.get_experiences(
                profile.id,
                public_only=public_only,
            )
        )

        return items, len(items)

    def get_experience(
        self,
        experience_id: int,
    ) -> Experience:
        profile = self._profile()

        experience = (
            self.repository.get_experience(
                experience_id
            )
        )

        if (
            experience is None
            or experience.profile_id
            != profile.id
        ):
            raise ResourceNotFoundError(
                "Experience not found"
            )

        return experience

    def create_experience(
        self,
        data: ExperienceCreate,
    ) -> Experience:
        profile = self._profile()

        organization = (
            self.repository.get_organization(
                data.organization_id
            )
        )

        if organization is None:
            raise ResourceNotFoundError(
                "Organization not found"
            )

        self._validate_dates(
            data.start_date,
            data.end_date,
        )

        experience = Experience(
            profile_id=profile.id,
            organization_id=(
                data.organization_id
            ),
            role_title=(
                data.role_title.strip()
            ),
            employment_type=(
                data.employment_type
            ),
            location=data.location,
            start_date=data.start_date,
            end_date=data.end_date,
            summary=data.summary,
            display_order=data.display_order,
            is_visible=data.is_visible,
        )

        return (
            self.repository.save_experience(
                experience
            )
        )

    def update_experience(
        self,
        experience_id: int,
        data: ExperienceUpdate,
    ) -> Experience:
        experience = self.get_experience(
            experience_id
        )

        changes = data.model_dump(
            exclude_unset=True
        )

        if "organization_id" in changes:
            organization_id = changes[
                "organization_id"
            ]

            if organization_id is None:
                raise DomainValidationError(
                    "Organization cannot be null"
                )

            if (
                self.repository.get_organization(
                    organization_id
                )
                is None
            ):
                raise ResourceNotFoundError(
                    "Organization not found"
                )

            experience.organization_id = (
                organization_id
            )

        if "role_title" in changes:
            if changes["role_title"] is None:
                raise DomainValidationError(
                    "Role title cannot be null"
                )

            experience.role_title = (
                changes["role_title"].strip()
            )

        new_start = changes.get(
            "start_date",
            experience.start_date,
        )

        if new_start is None:
            raise DomainValidationError(
                "Start date cannot be null"
            )

        new_end = (
            changes["end_date"]
            if "end_date" in changes
            else experience.end_date
        )

        self._validate_dates(
            new_start,
            new_end,
        )

        experience.start_date = new_start
        experience.end_date = new_end

        for field in (
            "employment_type",
            "location",
            "summary",
        ):
            if field in changes:
                setattr(
                    experience,
                    field,
                    changes[field],
                )

        for field in (
            "display_order",
            "is_visible",
        ):
            if field in changes:
                if changes[field] is None:
                    raise DomainValidationError(
                        f"{field} cannot be null"
                    )

                setattr(
                    experience,
                    field,
                    changes[field],
                )

        return (
            self.repository.save_experience(
                experience
            )
        )

    def delete_experience(
        self,
        experience_id: int,
    ):
        experience = self.get_experience(
            experience_id
        )

        self.repository.delete_experience(
            experience
        )

    # =====================================================
    # HIGHLIGHTS
    # =====================================================

    def create_highlight(
        self,
        experience_id: int,
        data: ExperienceHighlightCreate,
    ):
        self.get_experience(
            experience_id
        )

        highlight = ExperienceHighlight(
            experience_id=experience_id,
            content=data.content.strip(),
            display_order=data.display_order,
            is_visible=data.is_visible,
        )

        return self.repository.save_highlight(
            highlight
        )

    def update_highlight(
        self,
        experience_id: int,
        highlight_id: int,
        data: ExperienceHighlightUpdate,
    ):
        self.get_experience(
            experience_id
        )

        highlight = (
            self.repository.get_highlight(
                highlight_id
            )
        )

        if (
            highlight is None
            or highlight.experience_id
            != experience_id
        ):
            raise ResourceNotFoundError(
                "Experience highlight not found"
            )

        changes = data.model_dump(
            exclude_unset=True
        )

        if "content" in changes:
            if changes["content"] is None:
                raise DomainValidationError(
                    "Highlight content cannot be null"
                )

            highlight.content = (
                changes["content"].strip()
            )

        for field in (
            "display_order",
            "is_visible",
        ):
            if field in changes:
                if changes[field] is None:
                    raise DomainValidationError(
                        f"{field} cannot be null"
                    )

                setattr(
                    highlight,
                    field,
                    changes[field],
                )

        return self.repository.save_highlight(
            highlight
        )

    def delete_highlight(
        self,
        experience_id: int,
        highlight_id: int,
    ):
        self.get_experience(
            experience_id
        )

        highlight = (
            self.repository.get_highlight(
                highlight_id
            )
        )

        if (
            highlight is None
            or highlight.experience_id
            != experience_id
        ):
            raise ResourceNotFoundError(
                "Experience highlight not found"
            )

        self.repository.delete_highlight(
            highlight
        )

    # =====================================================
    # EXPERIENCE TECHNOLOGIES
    # =====================================================

    def add_technology(
        self,
        experience_id: int,
        data: ExperienceTechnologyCreate,
    ):
        self.get_experience(
            experience_id
        )

        technology = (
            self.repository.get_technology(
                data.technology_id
            )
        )

        if technology is None:
            raise ResourceNotFoundError(
                "Technology not found"
            )

        existing = (
            self.repository
            .get_experience_technology(
                experience_id,
                data.technology_id,
            )
        )

        if existing is not None:
            raise ResourceConflictError(
                "Technology is already associated with this experience"
            )

        association = ExperienceTechnology(
            experience_id=experience_id,
            technology_id=(
                data.technology_id
            ),
            display_order=(
                data.display_order
            ),
        )

        self.repository.save_experience_technology(
            association
        )

        # Re-fetch to return nested technology/category
        experience = self.get_experience(
            experience_id
        )

        return next(
            item
            for item in experience.technologies
            if item.technology_id
            == data.technology_id
        )

    def update_technology(
        self,
        experience_id: int,
        technology_id: int,
        data: ExperienceTechnologyUpdate,
    ):
        self.get_experience(
            experience_id
        )

        association = (
            self.repository
            .get_experience_technology(
                experience_id,
                technology_id,
            )
        )

        if association is None:
            raise ResourceNotFoundError(
                "Experience technology not found"
            )

        association.display_order = (
            data.display_order
        )

        self.repository.save_experience_technology(
            association
        )

        experience = self.get_experience(
            experience_id
        )

        return next(
            item
            for item in experience.technologies
            if item.technology_id
            == technology_id
        )

    def remove_technology(
        self,
        experience_id: int,
        technology_id: int,
    ):
        self.get_experience(
            experience_id
        )

        association = (
            self.repository
            .get_experience_technology(
                experience_id,
                technology_id,
            )
        )

        if association is None:
            raise ResourceNotFoundError(
                "Experience technology not found"
            )

        self.repository.delete_experience_technology(
            association
        )

    # =====================================================
    # EDUCATION
    # =====================================================

    def get_educations(
        self,
        public_only: bool = False,
    ):
        profile = self._profile()

        items = (
            self.repository.get_educations(
                profile.id,
                public_only=public_only,
            )
        )

        return items, len(items)

    def get_education(
        self,
        education_id: int,
    ) -> Education:
        profile = self._profile()

        education = (
            self.repository.get_education(
                education_id
            )
        )

        if (
            education is None
            or education.profile_id
            != profile.id
        ):
            raise ResourceNotFoundError(
                "Education not found"
            )

        return education

    def create_education(
        self,
        data: EducationCreate,
    ) -> Education:
        profile = self._profile()

        if (
            self.repository.get_organization(
                data.organization_id
            )
            is None
        ):
            raise ResourceNotFoundError(
                "Organization not found"
            )

        self._validate_dates(
            data.start_date,
            data.end_date,
        )

        education = Education(
            profile_id=profile.id,
            organization_id=(
                data.organization_id
            ),
            degree=data.degree.strip(),
            field_of_study=(
                data.field_of_study
            ),
            location=data.location,
            start_date=data.start_date,
            end_date=data.end_date,
            description=data.description,
            display_order=data.display_order,
            is_visible=data.is_visible,
        )

        return self.repository.save_education(
            education
        )

    def update_education(
        self,
        education_id: int,
        data: EducationUpdate,
    ) -> Education:
        education = self.get_education(
            education_id
        )

        changes = data.model_dump(
            exclude_unset=True
        )

        if "organization_id" in changes:
            organization_id = changes[
                "organization_id"
            ]

            if organization_id is None:
                raise DomainValidationError(
                    "Organization cannot be null"
                )

            if (
                self.repository.get_organization(
                    organization_id
                )
                is None
            ):
                raise ResourceNotFoundError(
                    "Organization not found"
                )

            education.organization_id = (
                organization_id
            )

        if "degree" in changes:
            if changes["degree"] is None:
                raise DomainValidationError(
                    "Degree cannot be null"
                )

            education.degree = (
                changes["degree"].strip()
            )

        new_start = changes.get(
            "start_date",
            education.start_date,
        )

        if new_start is None:
            raise DomainValidationError(
                "Start date cannot be null"
            )

        new_end = (
            changes["end_date"]
            if "end_date" in changes
            else education.end_date
        )

        self._validate_dates(
            new_start,
            new_end,
        )

        education.start_date = new_start
        education.end_date = new_end

        for field in (
            "field_of_study",
            "location",
            "description",
        ):
            if field in changes:
                setattr(
                    education,
                    field,
                    changes[field],
                )

        for field in (
            "display_order",
            "is_visible",
        ):
            if field in changes:
                if changes[field] is None:
                    raise DomainValidationError(
                        f"{field} cannot be null"
                    )

                setattr(
                    education,
                    field,
                    changes[field],
                )

        return self.repository.save_education(
            education
        )

    def delete_education(
        self,
        education_id: int,
    ):
        education = self.get_education(
            education_id
        )

        self.repository.delete_education(
            education
        )