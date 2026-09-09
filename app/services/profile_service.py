from app.core.exceptions import (
    DomainValidationError,
    ResourceConflictError,
    ResourceNotFoundError,
)
from app.models.interest import Interest
from app.models.profile import Profile
from app.models.profile_contact import ProfileContact
from app.models.social_link import SocialLink
from app.models.strength import Strength
from app.repositories.profile_repository import (
    ProfileRepository,
)
from app.schemas.profile import (
    InterestCreate,
    InterestUpdate,
    ProfileContactCreate,
    ProfileContactUpdate,
    ProfileCreate,
    ProfileUpdate,
    SocialLinkCreate,
    SocialLinkUpdate,
    StrengthCreate,
    StrengthUpdate,
)


class ProfileService:
    def __init__(
        self,
        repository: ProfileRepository,
    ):
        self.repository = repository

    # =====================================================
    # HELPERS
    # =====================================================

    def _require_profile(
        self,
    ) -> Profile:
        profile = self.repository.get_profile()

        if profile is None:
            raise ResourceNotFoundError(
                "Profile has not been created yet"
            )

        return profile

    # =====================================================
    # PROFILE
    # =====================================================

    def get_profile(
        self,
        public_only: bool = False,
    ) -> Profile:
        profile = self.repository.get_profile(
            public_only=public_only
        )

        if profile is None:
            raise ResourceNotFoundError(
                "Profile has not been created yet"
            )

        return profile

    def create_profile(
        self,
        data: ProfileCreate,
    ) -> Profile:
        existing = self.repository.get_profile()

        if existing is not None:
            raise ResourceConflictError(
                "A portfolio profile already exists"
            )

        profile = Profile(
            full_name=data.full_name.strip(),
            professional_title=(
                data.professional_title.strip()
            ),
            headline=data.headline,
            short_bio=data.short_bio,
            about=data.about,
            mission=data.mission,
            location=data.location,
            availability_text=(
                data.availability_text
            ),
        )

        return self.repository.create_profile(
            profile
        )

    def update_profile(
        self,
        data: ProfileUpdate,
    ) -> Profile:
        profile = self._require_profile()

        changes = data.model_dump(
            exclude_unset=True
        )

        required_fields = {
            "full_name",
            "professional_title",
        }

        for field in required_fields:
            if (
                field in changes
                and changes[field] is None
            ):
                raise DomainValidationError(
                    f"{field} cannot be null"
                )

        if "full_name" in changes:
            profile.full_name = (
                changes["full_name"].strip()
            )

        if "professional_title" in changes:
            profile.professional_title = (
                changes[
                    "professional_title"
                ].strip()
            )

        optional_fields = (
            "headline",
            "short_bio",
            "about",
            "mission",
            "location",
            "availability_text",
        )

        for field in optional_fields:
            if field in changes:
                setattr(
                    profile,
                    field,
                    changes[field],
                )

        return self.repository.update_profile(
            profile
        )

    # =====================================================
    # CONTACTS
    # =====================================================

    def create_contact(
        self,
        data: ProfileContactCreate,
    ) -> ProfileContact:
        profile = self._require_profile()

        contact_type = (
            data.contact_type.strip().upper()
        )

        allowed_types = {
            "EMAIL",
            "PHONE",
            "WHATSAPP",
            "OTHER",
        }

        if contact_type not in allowed_types:
            raise DomainValidationError(
                "Invalid contact type"
            )

        if data.is_primary:
            existing_primary = (
                self.repository.get_primary_contact(
                    profile.id,
                    contact_type,
                )
            )

            if existing_primary is not None:
                raise ResourceConflictError(
                    f"A primary {contact_type} already exists"
                )

        contact = ProfileContact(
            profile_id=profile.id,
            contact_type=contact_type,
            label=data.label,
            value=data.value.strip(),
            is_primary=data.is_primary,
            display_order=data.display_order,
            is_visible=data.is_visible,
        )

        return self.repository.create_contact(
            contact
        )

    def update_contact(
        self,
        contact_id: int,
        data: ProfileContactUpdate,
    ) -> ProfileContact:
        profile = self._require_profile()

        contact = (
            self.repository.get_contact_by_id(
                contact_id
            )
        )

        if (
            contact is None
            or contact.profile_id != profile.id
        ):
            raise ResourceNotFoundError(
                "Profile contact not found"
            )

        changes = data.model_dump(
            exclude_unset=True
        )

        if "contact_type" in changes:
            if changes["contact_type"] is None:
                raise DomainValidationError(
                    "Contact type cannot be null"
                )

            contact_type = (
                changes["contact_type"]
                .strip()
                .upper()
            )

            allowed_types = {
                "EMAIL",
                "PHONE",
                "WHATSAPP",
                "OTHER",
            }

            if contact_type not in allowed_types:
                raise DomainValidationError(
                    "Invalid contact type"
                )

            contact.contact_type = contact_type

        if "value" in changes:
            if changes["value"] is None:
                raise DomainValidationError(
                    "Contact value cannot be null"
                )

            contact.value = (
                changes["value"].strip()
            )

        for field in (
            "label",
            "display_order",
            "is_visible",
        ):
            if field in changes:
                setattr(
                    contact,
                    field,
                    changes[field],
                )

        if "is_primary" in changes:
            new_primary = changes["is_primary"]

            if new_primary is None:
                raise DomainValidationError(
                    "is_primary cannot be null"
                )

            if new_primary:
                existing = (
                    self.repository
                    .get_primary_contact(
                        profile.id,
                        contact.contact_type,
                    )
                )

                if (
                    existing is not None
                    and existing.id != contact.id
                ):
                    raise ResourceConflictError(
                        f"A primary {contact.contact_type} already exists"
                    )

            contact.is_primary = new_primary

        return self.repository.update_contact(
            contact
        )

    def delete_contact(
        self,
        contact_id: int,
    ) -> None:
        profile = self._require_profile()

        contact = (
            self.repository.get_contact_by_id(
                contact_id
            )
        )

        if (
            contact is None
            or contact.profile_id != profile.id
        ):
            raise ResourceNotFoundError(
                "Profile contact not found"
            )

        self.repository.delete_contact(
            contact
        )

    # =====================================================
    # SOCIAL LINKS
    # =====================================================

    def create_social_link(
        self,
        data: SocialLinkCreate,
    ) -> SocialLink:
        profile = self._require_profile()

        url = data.url.strip()

        existing = (
            self.repository
            .get_social_link_by_url(
                profile.id,
                url,
            )
        )

        if existing is not None:
            raise ResourceConflictError(
                "This social link already exists"
            )

        social_link = SocialLink(
            profile_id=profile.id,
            platform=data.platform.strip(),
            label=data.label,
            url=url,
            display_order=data.display_order,
            is_visible=data.is_visible,
        )

        return (
            self.repository
            .create_social_link(
                social_link
            )
        )

    def update_social_link(
        self,
        social_link_id: int,
        data: SocialLinkUpdate,
    ) -> SocialLink:
        profile = self._require_profile()

        social_link = (
            self.repository
            .get_social_link_by_id(
                social_link_id
            )
        )

        if (
            social_link is None
            or social_link.profile_id
            != profile.id
        ):
            raise ResourceNotFoundError(
                "Social link not found"
            )

        changes = data.model_dump(
            exclude_unset=True
        )

        for required in (
            "platform",
            "url",
        ):
            if (
                required in changes
                and changes[required] is None
            ):
                raise DomainValidationError(
                    f"{required} cannot be null"
                )

        if "platform" in changes:
            social_link.platform = (
                changes["platform"].strip()
            )

        if "url" in changes:
            new_url = changes["url"].strip()

            existing = (
                self.repository
                .get_social_link_by_url(
                    profile.id,
                    new_url,
                )
            )

            if (
                existing is not None
                and existing.id
                != social_link.id
            ):
                raise ResourceConflictError(
                    "This social link already exists"
                )

            social_link.url = new_url

        for field in (
            "label",
            "display_order",
            "is_visible",
        ):
            if field in changes:
                setattr(
                    social_link,
                    field,
                    changes[field],
                )

        return (
            self.repository
            .update_social_link(
                social_link
            )
        )

    def delete_social_link(
        self,
        social_link_id: int,
    ) -> None:
        profile = self._require_profile()

        social_link = (
            self.repository
            .get_social_link_by_id(
                social_link_id
            )
        )

        if (
            social_link is None
            or social_link.profile_id
            != profile.id
        ):
            raise ResourceNotFoundError(
                "Social link not found"
            )

        self.repository.delete_social_link(
            social_link
        )

    # =====================================================
    # STRENGTHS
    # =====================================================

    def create_strength(
        self,
        data: StrengthCreate,
    ) -> Strength:
        profile = self._require_profile()

        strength = Strength(
            profile_id=profile.id,
            title=data.title.strip(),
            description=data.description,
            display_order=data.display_order,
            is_visible=data.is_visible,
        )

        return (
            self.repository
            .create_strength(
                strength
            )
        )

    def update_strength(
        self,
        strength_id: int,
        data: StrengthUpdate,
    ) -> Strength:
        profile = self._require_profile()

        strength = (
            self.repository.get_strength_by_id(
                strength_id
            )
        )

        if (
            strength is None
            or strength.profile_id
            != profile.id
        ):
            raise ResourceNotFoundError(
                "Strength not found"
            )

        changes = data.model_dump(
            exclude_unset=True
        )

        if "title" in changes:
            if changes["title"] is None:
                raise DomainValidationError(
                    "Strength title cannot be null"
                )

            strength.title = (
                changes["title"].strip()
            )

        for field in (
            "description",
            "display_order",
            "is_visible",
        ):
            if field in changes:
                setattr(
                    strength,
                    field,
                    changes[field],
                )

        return (
            self.repository
            .update_strength(
                strength
            )
        )

    def delete_strength(
        self,
        strength_id: int,
    ) -> None:
        profile = self._require_profile()

        strength = (
            self.repository.get_strength_by_id(
                strength_id
            )
        )

        if (
            strength is None
            or strength.profile_id
            != profile.id
        ):
            raise ResourceNotFoundError(
                "Strength not found"
            )

        self.repository.delete_strength(
            strength
        )

    # =====================================================
    # INTERESTS
    # =====================================================

    def create_interest(
        self,
        data: InterestCreate,
    ) -> Interest:
        profile = self._require_profile()

        interest = Interest(
            profile_id=profile.id,
            name=data.name.strip(),
            description=data.description,
            display_order=data.display_order,
            is_visible=data.is_visible,
        )

        return (
            self.repository
            .create_interest(
                interest
            )
        )

    def update_interest(
        self,
        interest_id: int,
        data: InterestUpdate,
    ) -> Interest:
        profile = self._require_profile()

        interest = (
            self.repository.get_interest_by_id(
                interest_id
            )
        )

        if (
            interest is None
            or interest.profile_id
            != profile.id
        ):
            raise ResourceNotFoundError(
                "Interest not found"
            )

        changes = data.model_dump(
            exclude_unset=True
        )

        if "name" in changes:
            if changes["name"] is None:
                raise DomainValidationError(
                    "Interest name cannot be null"
                )

            interest.name = (
                changes["name"].strip()
            )

        for field in (
            "description",
            "display_order",
            "is_visible",
        ):
            if field in changes:
                setattr(
                    interest,
                    field,
                    changes[field],
                )

        return (
            self.repository
            .update_interest(
                interest
            )
        )

    def delete_interest(
        self,
        interest_id: int,
    ) -> None:
        profile = self._require_profile()

        interest = (
            self.repository.get_interest_by_id(
                interest_id
            )
        )

        if (
            interest is None
            or interest.profile_id
            != profile.id
        ):
            raise ResourceNotFoundError(
                "Interest not found"
            )

        self.repository.delete_interest(
            interest
        )