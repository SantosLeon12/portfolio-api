from sqlalchemy import select
from sqlalchemy.orm import (
    Session,
    selectinload,
    with_loader_criteria,
)


from app.models.interest import Interest
from app.models.profile import Profile
from app.models.profile_contact import ProfileContact
from app.models.social_link import SocialLink
from app.models.strength import Strength


class ProfileRepository:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    # =====================================================
    # PROFILE
    # =====================================================

    def get_profile(
        self,
        public_only: bool = False,
    ) -> Profile | None:
        options = [
            selectinload(Profile.contacts),
            selectinload(Profile.social_links),
            selectinload(Profile.strengths),
            selectinload(Profile.interests),
        ]

        if public_only:
            options.extend([
                with_loader_criteria(
                    ProfileContact,
                    ProfileContact.is_visible.is_(True),
                    include_aliases=True,
                ),
                with_loader_criteria(
                    SocialLink,
                    SocialLink.is_visible.is_(True),
                    include_aliases=True,
                ),
                with_loader_criteria(
                    Strength,
                    Strength.is_visible.is_(True),
                    include_aliases=True,
                ),
                with_loader_criteria(
                    Interest,
                    Interest.is_visible.is_(True),
                    include_aliases=True,
                ),
            ])

        statement = (
            select(Profile)
            .options(*options)
            .order_by(Profile.id.asc())
            .limit(1)
        )

        return self.db.scalar(statement)

    def create_profile(
        self,
        profile: Profile,
    ) -> Profile:
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)

        return self.get_profile()

    def update_profile(
        self,
        profile: Profile,
    ) -> Profile:
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)

        return self.get_profile()

    # =====================================================
    # CONTACTS
    # =====================================================

    def get_contact_by_id(
        self,
        contact_id: int,
    ) -> ProfileContact | None:
        return self.db.get(
            ProfileContact,
            contact_id,
        )

    def create_contact(
        self,
        contact: ProfileContact,
    ) -> ProfileContact:
        self.db.add(contact)
        self.db.commit()
        self.db.refresh(contact)

        return contact

    def update_contact(
        self,
        contact: ProfileContact,
    ) -> ProfileContact:
        self.db.add(contact)
        self.db.commit()
        self.db.refresh(contact)

        return contact

    def delete_contact(
        self,
        contact: ProfileContact,
    ) -> None:
        self.db.delete(contact)
        self.db.commit()

    def get_primary_contact(
        self,
        profile_id: int,
        contact_type: str,
    ) -> ProfileContact | None:
        statement = select(
            ProfileContact
        ).where(
            ProfileContact.profile_id
            == profile_id,
            ProfileContact.contact_type
            == contact_type,
            ProfileContact.is_primary.is_(True),
        )

        return self.db.scalar(statement)

    # =====================================================
    # SOCIAL LINKS
    # =====================================================

    def get_social_link_by_id(
        self,
        social_link_id: int,
    ) -> SocialLink | None:
        return self.db.get(
            SocialLink,
            social_link_id,
        )

    def get_social_link_by_url(
        self,
        profile_id: int,
        url: str,
    ) -> SocialLink | None:
        statement = select(
            SocialLink
        ).where(
            SocialLink.profile_id
            == profile_id,
            SocialLink.url == url,
        )

        return self.db.scalar(statement)

    def create_social_link(
        self,
        social_link: SocialLink,
    ) -> SocialLink:
        self.db.add(social_link)
        self.db.commit()
        self.db.refresh(social_link)

        return social_link

    def update_social_link(
        self,
        social_link: SocialLink,
    ) -> SocialLink:
        self.db.add(social_link)
        self.db.commit()
        self.db.refresh(social_link)

        return social_link

    def delete_social_link(
        self,
        social_link: SocialLink,
    ) -> None:
        self.db.delete(social_link)
        self.db.commit()

    # =====================================================
    # STRENGTHS
    # =====================================================

    def get_strength_by_id(
        self,
        strength_id: int,
    ) -> Strength | None:
        return self.db.get(
            Strength,
            strength_id,
        )

    def create_strength(
        self,
        strength: Strength,
    ) -> Strength:
        self.db.add(strength)
        self.db.commit()
        self.db.refresh(strength)

        return strength

    def update_strength(
        self,
        strength: Strength,
    ) -> Strength:
        self.db.add(strength)
        self.db.commit()
        self.db.refresh(strength)

        return strength

    def delete_strength(
        self,
        strength: Strength,
    ) -> None:
        self.db.delete(strength)
        self.db.commit()

    # =====================================================
    # INTERESTS
    # =====================================================

    def get_interest_by_id(
        self,
        interest_id: int,
    ) -> Interest | None:
        return self.db.get(
            Interest,
            interest_id,
        )

    def create_interest(
        self,
        interest: Interest,
    ) -> Interest:
        self.db.add(interest)
        self.db.commit()
        self.db.refresh(interest)

        return interest

    def update_interest(
        self,
        interest: Interest,
    ) -> Interest:
        self.db.add(interest)
        self.db.commit()
        self.db.refresh(interest)

        return interest

    def delete_interest(
        self,
        interest: Interest,
    ) -> None:
        self.db.delete(interest)
        self.db.commit()