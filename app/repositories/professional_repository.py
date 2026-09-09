from sqlalchemy import func, select
from sqlalchemy.orm import (
    Session,
    selectinload,
    with_loader_criteria,
)

from app.models.education import Education
from app.models.experience import Experience
from app.models.experience_highlight import (
    ExperienceHighlight,
)
from app.models.experience_technology import (
    ExperienceTechnology,
)
from app.models.organization import Organization
from app.models.profile import Profile
from app.models.technology import Technology


class ProfessionalRepository:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    # =====================================================
    # COMMON
    # =====================================================

    def get_profile(
        self,
    ) -> Profile | None:
        statement = (
            select(Profile)
            .order_by(Profile.id.asc())
            .limit(1)
        )

        return self.db.scalar(statement)

    def get_organization(
        self,
        organization_id: int,
    ) -> Organization | None:
        return self.db.get(
            Organization,
            organization_id,
        )

    def get_technology(
        self,
        technology_id: int,
    ) -> Technology | None:
        return self.db.get(
            Technology,
            technology_id,
        )

    # =====================================================
    # EXPERIENCES
    # =====================================================

    def _experience_options(
        self,
        public_only: bool = False,
    ):
        options = [
            selectinload(
                Experience.organization
            ),
            selectinload(
                Experience.highlights
            ),
            (
                selectinload(
                    Experience.technologies
                )
                .selectinload(
                    ExperienceTechnology.technology
                )
                .selectinload(
                    Technology.category
                )
            ),
        ]

        if public_only:
            options.append(
                with_loader_criteria(
                    ExperienceHighlight,
                    ExperienceHighlight.is_visible.is_(
                        True
                    ),
                    include_aliases=True,
                )
            )

        return options

    def get_experiences(
        self,
        profile_id: int,
        public_only: bool = False,
    ) -> list[Experience]:
        statement = (
            select(Experience)
            .options(
                *self._experience_options(
                    public_only
                )
            )
            .where(
                Experience.profile_id
                == profile_id
            )
        )

        if public_only:
            statement = statement.where(
                Experience.is_visible.is_(
                    True
                )
            )

        statement = statement.order_by(
            Experience.display_order.asc(),
            Experience.start_date.desc(),
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get_experience(
        self,
        experience_id: int,
    ) -> Experience | None:
        statement = (
            select(Experience)
            .options(
                *self._experience_options()
            )
            .where(
                Experience.id
                == experience_id
            )
        )

        return self.db.scalar(statement)

    def save_experience(
        self,
        experience: Experience,
    ) -> Experience:
        self.db.add(experience)
        self.db.commit()

        return self.get_experience(
            experience.id
        )

    def delete_experience(
        self,
        experience: Experience,
    ) -> None:
        self.db.delete(experience)
        self.db.commit()

    # =====================================================
    # HIGHLIGHTS
    # =====================================================

    def get_highlight(
        self,
        highlight_id: int,
    ) -> ExperienceHighlight | None:
        return self.db.get(
            ExperienceHighlight,
            highlight_id,
        )

    def save_highlight(
        self,
        highlight: ExperienceHighlight,
    ) -> ExperienceHighlight:
        self.db.add(highlight)
        self.db.commit()
        self.db.refresh(highlight)

        return highlight

    def delete_highlight(
        self,
        highlight: ExperienceHighlight,
    ) -> None:
        self.db.delete(highlight)
        self.db.commit()

    # =====================================================
    # EXPERIENCE TECHNOLOGIES
    # =====================================================

    def get_experience_technology(
        self,
        experience_id: int,
        technology_id: int,
    ) -> ExperienceTechnology | None:
        statement = select(
            ExperienceTechnology
        ).where(
            ExperienceTechnology.experience_id
            == experience_id,
            ExperienceTechnology.technology_id
            == technology_id,
        )

        return self.db.scalar(statement)

    def save_experience_technology(
        self,
        association: ExperienceTechnology,
    ) -> ExperienceTechnology:
        self.db.add(association)
        self.db.commit()
        self.db.refresh(association)

        return association

    def delete_experience_technology(
        self,
        association: ExperienceTechnology,
    ) -> None:
        self.db.delete(association)
        self.db.commit()

    # =====================================================
    # EDUCATION
    # =====================================================

    def get_educations(
        self,
        profile_id: int,
        public_only: bool = False,
    ) -> list[Education]:
        statement = (
            select(Education)
            .options(
                selectinload(
                    Education.organization
                )
            )
            .where(
                Education.profile_id
                == profile_id
            )
        )

        if public_only:
            statement = statement.where(
                Education.is_visible.is_(
                    True
                )
            )

        statement = statement.order_by(
            Education.display_order.asc(),
            Education.start_date.desc(),
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get_education(
        self,
        education_id: int,
    ) -> Education | None:
        statement = (
            select(Education)
            .options(
                selectinload(
                    Education.organization
                )
            )
            .where(
                Education.id
                == education_id
            )
        )

        return self.db.scalar(statement)

    def save_education(
        self,
        education: Education,
    ) -> Education:
        self.db.add(education)
        self.db.commit()

        return self.get_education(
            education.id
        )

    def delete_education(
        self,
        education: Education,
    ) -> None:
        self.db.delete(education)
        self.db.commit()