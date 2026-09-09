from sqlalchemy import func, select
from sqlalchemy.orm import (
    Session,
    selectinload,
)

from app.models.language import Language
from app.models.profile import Profile
from app.models.profile_language import (
    ProfileLanguage,
)
from app.models.proficiency_level import (
    ProficiencyLevel,
)


class LanguageRepository:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def get_profile(self):
        return self.db.scalar(
            select(Profile)
            .order_by(Profile.id.asc())
            .limit(1)
        )

    # LANGUAGES

    def get_languages(self):
        return list(
            self.db.scalars(
                select(Language)
                .order_by(
                    Language.name.asc()
                )
            ).all()
        )

    def get_language(
        self,
        language_id: int,
    ):
        return self.db.get(
            Language,
            language_id,
        )

    def get_language_by_name(
        self,
        name: str,
    ):
        return self.db.scalar(
            select(Language).where(
                func.lower(Language.name)
                == name.lower()
            )
        )

    def get_language_by_code(
        self,
        code: str,
    ):
        return self.db.scalar(
            select(Language).where(
                Language.iso_code == code
            )
        )

    def save_language(
        self,
        language: Language,
    ):
        self.db.add(language)
        self.db.commit()
        self.db.refresh(language)
        return language

    def delete_language(
        self,
        language: Language,
    ):
        self.db.delete(language)
        self.db.commit()

    def count_language_usage(
        self,
        language_id: int,
    ) -> int:
        return (
            self.db.scalar(
                select(func.count())
                .select_from(ProfileLanguage)
                .where(
                    ProfileLanguage.language_id
                    == language_id
                )
            )
            or 0
        )

    # LEVELS

    def get_levels(self):
        return list(
            self.db.scalars(
                select(ProficiencyLevel)
                .order_by(
                    ProficiencyLevel.rank.asc()
                )
            ).all()
        )

    def get_level(
        self,
        level_id: int,
    ):
        return self.db.get(
            ProficiencyLevel,
            level_id,
        )

    def get_level_by_code(
        self,
        code: str,
    ):
        return self.db.scalar(
            select(ProficiencyLevel).where(
                ProficiencyLevel.code == code
            )
        )

    def get_level_by_rank(
        self,
        rank: int,
    ):
        return self.db.scalar(
            select(ProficiencyLevel).where(
                ProficiencyLevel.rank == rank
            )
        )

    def save_level(
        self,
        level: ProficiencyLevel,
    ):
        self.db.add(level)
        self.db.commit()
        self.db.refresh(level)
        return level

    def delete_level(
        self,
        level: ProficiencyLevel,
    ):
        self.db.delete(level)
        self.db.commit()

    def count_level_usage(
        self,
        level_id: int,
    ) -> int:
        return (
            self.db.scalar(
                select(func.count())
                .select_from(ProfileLanguage)
                .where(
                    ProfileLanguage.proficiency_level_id
                    == level_id
                )
            )
            or 0
        )

    # PROFILE LANGUAGES

    def get_profile_languages(
        self,
        profile_id: int,
    ):
        statement = (
            select(ProfileLanguage)
            .options(
                selectinload(
                    ProfileLanguage.language
                ),
                selectinload(
                    ProfileLanguage
                    .proficiency_level
                ),
            )
            .where(
                ProfileLanguage.profile_id
                == profile_id
            )
            .order_by(
                ProfileLanguage
                .display_order.asc()
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get_profile_language(
        self,
        profile_id: int,
        language_id: int,
    ):
        statement = (
            select(ProfileLanguage)
            .options(
                selectinload(
                    ProfileLanguage.language
                ),
                selectinload(
                    ProfileLanguage
                    .proficiency_level
                ),
            )
            .where(
                ProfileLanguage.profile_id
                == profile_id,
                ProfileLanguage.language_id
                == language_id,
            )
        )

        return self.db.scalar(statement)

    def save_profile_language(
        self,
        association: ProfileLanguage,
    ):
        self.db.add(association)
        self.db.commit()

        return self.get_profile_language(
            association.profile_id,
            association.language_id,
        )

    def delete_profile_language(
        self,
        association: ProfileLanguage,
    ):
        self.db.delete(association)
        self.db.commit()