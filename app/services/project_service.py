from datetime import datetime, timezone

from app.core.exceptions import (
    DomainValidationError,
    ResourceConflictError,
    ResourceInUseError,
    ResourceNotFoundError,
)
from app.models.project import Project
from app.models.project_category import ProjectCategory
from app.models.project_category_relation import (
    ProjectCategoryRelation,
)
from app.models.project_link import ProjectLink
from app.models.project_media import ProjectMedia
from app.models.project_section import ProjectSection
from app.models.project_section_item import (
    ProjectSectionItem,
)
from app.models.project_technology import (
    ProjectTechnology,
)
from app.repositories.project_repository import (
    ProjectRepository,
)
from app.schemas.project import (
    ProjectCategoryCreate,
    ProjectCategoryUpdate,
    ProjectCreate,
    ProjectLinkCreate,
    ProjectLinkUpdate,
    ProjectMediaCreate,
    ProjectMediaUpdate,
    ProjectSectionCreate,
    ProjectSectionItemCreate,
    ProjectSectionItemUpdate,
    ProjectSectionUpdate,
    ProjectTechnologyCreate,
    ProjectTechnologyUpdate,
    ProjectUpdate,
)


class ProjectService:
    STATUSES = {
        "DRAFT",
        "PUBLISHED",
        "ARCHIVED",
    }

    LINK_TYPES = {
        "REPOSITORY",
        "LIVE_DEMO",
        "DOCUMENTATION",
        "CASE_STUDY",
        "OTHER",
    }

    MEDIA_ROLES = {
        "COVER",
        "SCREENSHOT",
        "GALLERY",
        "DIAGRAM",
        "LOGO",
        "OTHER",
    }

    SECTION_TYPES = {
        "OVERVIEW",
        "PROBLEM",
        "RESPONSIBILITIES",
        "SOLUTION",
        "ARCHITECTURE",
        "CHALLENGES",
        "RESULTS",
        "LEARNINGS",
        "CUSTOM",
    }

    def __init__(
        self,
        repository: ProjectRepository,
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
            start_date is not None
            and end_date is not None
            and end_date < start_date
        ):
            raise DomainValidationError(
                "End date cannot be earlier than start date"
            )

    # =====================================================
    # CATEGORIES
    # =====================================================

    def get_categories(self):
        return self.repository.get_categories()

    def create_category(
        self,
        data: ProjectCategoryCreate,
    ):
        name = data.name.strip()
        slug = data.slug.strip().lower()

        if self.repository.get_category_by_name(
            name
        ):
            raise ResourceConflictError(
                "Project category already exists"
            )

        if self.repository.get_category_by_slug(
            slug
        ):
            raise ResourceConflictError(
                "Project category slug already exists"
            )

        return self.repository.save_category(
            ProjectCategory(
                name=name,
                slug=slug,
                display_order=data.display_order,
            )
        )

    def update_category(
        self,
        category_id: int,
        data: ProjectCategoryUpdate,
    ):
        category = self.repository.get_category(
            category_id
        )

        if category is None:
            raise ResourceNotFoundError(
                "Project category not found"
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
                    "Project category already exists"
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
                    "Project category slug already exists"
                )

            category.slug = slug

        if "display_order" in changes:
            if changes["display_order"] is None:
                raise DomainValidationError(
                    "Display order cannot be null"
                )

            category.display_order = (
                changes["display_order"]
            )

        return self.repository.save_category(
            category
        )

    def delete_category(
        self,
        category_id: int,
    ):
        category = self.repository.get_category(
            category_id
        )

        if category is None:
            raise ResourceNotFoundError(
                "Project category not found"
            )

        if (
            self.repository.count_category_usage(
                category_id
            )
            > 0
        ):
            raise ResourceInUseError(
                "Project category is currently in use"
            )

        self.repository.delete_category(
            category
        )

    # =====================================================
    # PROJECT
    # =====================================================

    def get_projects(
        self,
        public_only: bool = False,
        featured: bool | None = None,
    ):
        profile = self._profile()

        items = self.repository.get_projects(
            profile.id,
            public_only=public_only,
            featured=featured,
        )

        return items, len(items)

    def get_project(
        self,
        project_id: int,
    ):
        profile = self._profile()

        project = self.repository.get_project(
            project_id
        )

        if (
            project is None
            or project.profile_id
            != profile.id
        ):
            raise ResourceNotFoundError(
                "Project not found"
            )

        return project

    def get_public_by_slug(
        self,
        slug: str,
    ):
        project = self.repository.get_by_slug(
            slug,
            public_only=True,
        )

        if project is None:
            raise ResourceNotFoundError(
                "Project not found"
            )

        return project

    def create_project(
        self,
        data: ProjectCreate,
    ):
        profile = self._profile()

        slug = data.slug.strip().lower()

        if self.repository.get_by_slug(slug):
            raise ResourceConflictError(
                "Project slug already exists"
            )

        if data.organization_id is not None:
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

        project_status = (
            data.status.strip().upper()
        )

        if project_status not in self.STATUSES:
            raise DomainValidationError(
                "Invalid project status"
            )

        published_at = None

        if project_status == "PUBLISHED":
            published_at = datetime.now(
                timezone.utc
            )

        project = Project(
            profile_id=profile.id,
            organization_id=data.organization_id,
            title=data.title.strip(),
            slug=slug,
            short_description=(
                data.short_description
            ),
            overview=data.overview,
            role_summary=data.role_summary,
            start_date=data.start_date,
            end_date=data.end_date,
            status=project_status,
            featured=data.featured,
            display_order=data.display_order,
            published_at=published_at,
        )

        return self.repository.save_project(
            project
        )

    def update_project(
        self,
        project_id: int,
        data: ProjectUpdate,
    ):
        project = self.get_project(
            project_id
        )

        changes = data.model_dump(
            exclude_unset=True
        )

        if "organization_id" in changes:
            organization_id = changes[
                "organization_id"
            ]

            if organization_id is not None:
                if (
                    self.repository
                    .get_organization(
                        organization_id
                    )
                    is None
                ):
                    raise ResourceNotFoundError(
                        "Organization not found"
                    )

            project.organization_id = (
                organization_id
            )

        if "title" in changes:
            if changes["title"] is None:
                raise DomainValidationError(
                    "Project title cannot be null"
                )

            project.title = (
                changes["title"].strip()
            )

        if "slug" in changes:
            if changes["slug"] is None:
                raise DomainValidationError(
                    "Project slug cannot be null"
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
                and existing.id != project.id
            ):
                raise ResourceConflictError(
                    "Project slug already exists"
                )

            project.slug = slug

        new_start = changes.get(
            "start_date",
            project.start_date,
        )

        new_end = (
            changes["end_date"]
            if "end_date" in changes
            else project.end_date
        )

        self._validate_dates(
            new_start,
            new_end,
        )

        project.start_date = new_start
        project.end_date = new_end

        for field in (
            "short_description",
            "overview",
            "role_summary",
        ):
            if field in changes:
                setattr(
                    project,
                    field,
                    changes[field],
                )

        if "status" in changes:
            if changes["status"] is None:
                raise DomainValidationError(
                    "Project status cannot be null"
                )

            project_status = (
                changes["status"]
                .strip()
                .upper()
            )

            if project_status not in self.STATUSES:
                raise DomainValidationError(
                    "Invalid project status"
                )

            if (
                project_status == "PUBLISHED"
                and project.published_at is None
            ):
                project.published_at = (
                    datetime.now(
                        timezone.utc
                    )
                )

            if project_status == "DRAFT":
                project.published_at = None

            project.status = project_status

        for field in (
            "featured",
            "display_order",
        ):
            if field in changes:
                if changes[field] is None:
                    raise DomainValidationError(
                        f"{field} cannot be null"
                    )

                setattr(
                    project,
                    field,
                    changes[field],
                )

        return self.repository.save_project(
            project
        )

    def delete_project(
        self,
        project_id: int,
    ):
        project = self.get_project(
            project_id
        )

        self.repository.delete_project(
            project
        )

    # =====================================================
    # CATEGORY RELATION
    # =====================================================

    def add_category(
        self,
        project_id: int,
        category_id: int,
    ):
        self.get_project(project_id)

        category = self.repository.get_category(
            category_id
        )

        if category is None:
            raise ResourceNotFoundError(
                "Project category not found"
            )

        if (
            self.repository
            .get_category_relation(
                project_id,
                category_id,
            )
            is not None
        ):
            raise ResourceConflictError(
                "Category is already assigned to project"
            )

        self.repository.save_category_relation(
            ProjectCategoryRelation(
                project_id=project_id,
                category_id=category_id,
            )
        )

        return self.get_project(project_id)

    def remove_category(
        self,
        project_id: int,
        category_id: int,
    ):
        self.get_project(project_id)

        relation = (
            self.repository
            .get_category_relation(
                project_id,
                category_id,
            )
        )

        if relation is None:
            raise ResourceNotFoundError(
                "Project category relation not found"
            )

        self.repository.delete_category_relation(
            relation
        )

    # =====================================================
    # TECHNOLOGIES
    # =====================================================

    def add_technology(
        self,
        project_id: int,
        data: ProjectTechnologyCreate,
    ):
        self.get_project(project_id)

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
            self.repository
            .get_project_technology(
                project_id,
                data.technology_id,
            )
            is not None
        ):
            raise ResourceConflictError(
                "Technology is already assigned to project"
            )

        return (
            self.repository
            .save_project_technology(
                ProjectTechnology(
                    project_id=project_id,
                    technology_id=(
                        data.technology_id
                    ),
                    display_order=(
                        data.display_order
                    ),
                )
            )
        )

    def update_technology(
        self,
        project_id: int,
        technology_id: int,
        data: ProjectTechnologyUpdate,
    ):
        self.get_project(project_id)

        item = (
            self.repository
            .get_project_technology(
                project_id,
                technology_id,
            )
        )

        if item is None:
            raise ResourceNotFoundError(
                "Project technology not found"
            )

        item.display_order = (
            data.display_order
        )

        return (
            self.repository
            .save_project_technology(
                item
            )
        )

    def remove_technology(
        self,
        project_id: int,
        technology_id: int,
    ):
        self.get_project(project_id)

        item = (
            self.repository
            .get_project_technology(
                project_id,
                technology_id,
            )
        )

        if item is None:
            raise ResourceNotFoundError(
                "Project technology not found"
            )

        self.repository.delete_project_technology(
            item
        )

    # =====================================================
    # LINKS
    # =====================================================

    def create_link(
        self,
        project_id: int,
        data: ProjectLinkCreate,
    ):
        self.get_project(project_id)

        link_type = (
            data.link_type.strip().upper()
        )

        if link_type not in self.LINK_TYPES:
            raise DomainValidationError(
                "Invalid project link type"
            )

        url = data.url.strip()

        if (
            self.repository.get_link_by_url(
                project_id,
                url,
            )
            is not None
        ):
            raise ResourceConflictError(
                "Project link already exists"
            )

        return self.repository.save_link(
            ProjectLink(
                project_id=project_id,
                link_type=link_type,
                label=data.label,
                url=url,
                display_order=(
                    data.display_order
                ),
                is_visible=data.is_visible,
            )
        )

    def update_link(
        self,
        project_id: int,
        link_id: int,
        data: ProjectLinkUpdate,
    ):
        self.get_project(project_id)

        link = self.repository.get_link(
            link_id
        )

        if (
            link is None
            or link.project_id != project_id
        ):
            raise ResourceNotFoundError(
                "Project link not found"
            )

        changes = data.model_dump(
            exclude_unset=True
        )

        if "link_type" in changes:
            if changes["link_type"] is None:
                raise DomainValidationError(
                    "Link type cannot be null"
                )

            link_type = (
                changes["link_type"]
                .strip()
                .upper()
            )

            if link_type not in self.LINK_TYPES:
                raise DomainValidationError(
                    "Invalid project link type"
                )

            link.link_type = link_type

        if "url" in changes:
            if changes["url"] is None:
                raise DomainValidationError(
                    "URL cannot be null"
                )

            url = changes["url"].strip()

            existing = (
                self.repository
                .get_link_by_url(
                    project_id,
                    url,
                )
            )

            if (
                existing is not None
                and existing.id != link.id
            ):
                raise ResourceConflictError(
                    "Project link already exists"
                )

            link.url = url

        for field in (
            "label",
            "display_order",
            "is_visible",
        ):
            if field in changes:
                setattr(
                    link,
                    field,
                    changes[field],
                )

        return self.repository.save_link(
            link
        )

    def delete_link(
        self,
        project_id: int,
        link_id: int,
    ):
        self.get_project(project_id)

        link = self.repository.get_link(
            link_id
        )

        if (
            link is None
            or link.project_id != project_id
        ):
            raise ResourceNotFoundError(
                "Project link not found"
            )

        self.repository.delete_link(link)

    # =====================================================
    # MEDIA
    # =====================================================

    def create_media(
        self,
        project_id: int,
        data: ProjectMediaCreate,
    ):
        self.get_project(project_id)

        if (
            self.repository.get_media(
                data.media_asset_id
            )
            is None
        ):
            raise ResourceNotFoundError(
                "Media asset not found"
            )

        role = data.media_role.strip().upper()

        if role not in self.MEDIA_ROLES:
            raise DomainValidationError(
                "Invalid project media role"
            )

        if (
            self.repository
            .get_project_media_by_asset(
                project_id,
                data.media_asset_id,
            )
            is not None
        ):
            raise ResourceConflictError(
                "Media asset is already assigned to project"
            )

        return (
            self.repository.save_project_media(
                ProjectMedia(
                    project_id=project_id,
                    media_asset_id=(
                        data.media_asset_id
                    ),
                    media_role=role,
                    alt_text=data.alt_text,
                    caption=data.caption,
                    display_order=(
                        data.display_order
                    ),
                    is_visible=data.is_visible,
                )
            )
        )

    def update_media(
        self,
        project_id: int,
        project_media_id: int,
        data: ProjectMediaUpdate,
    ):
        self.get_project(project_id)

        item = (
            self.repository.get_project_media(
                project_media_id
            )
        )

        if (
            item is None
            or item.project_id != project_id
        ):
            raise ResourceNotFoundError(
                "Project media not found"
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

            if role not in self.MEDIA_ROLES:
                raise DomainValidationError(
                    "Invalid project media role"
                )

            item.media_role = role

        for field in (
            "alt_text",
            "caption",
            "display_order",
            "is_visible",
        ):
            if field in changes:
                setattr(
                    item,
                    field,
                    changes[field],
                )

        return (
            self.repository.save_project_media(
                item
            )
        )

    def delete_media(
        self,
        project_id: int,
        project_media_id: int,
    ):
        self.get_project(project_id)

        item = (
            self.repository.get_project_media(
                project_media_id
            )
        )

        if (
            item is None
            or item.project_id != project_id
        ):
            raise ResourceNotFoundError(
                "Project media not found"
            )

        self.repository.delete_project_media(
            item
        )

    # =====================================================
    # SECTIONS
    # =====================================================

    def create_section(
        self,
        project_id: int,
        data: ProjectSectionCreate,
    ):
        self.get_project(project_id)

        section_type = (
            data.section_type
            .strip()
            .upper()
        )

        if (
            section_type
            not in self.SECTION_TYPES
        ):
            raise DomainValidationError(
                "Invalid project section type"
            )

        return self.repository.save_section(
            ProjectSection(
                project_id=project_id,
                section_type=section_type,
                title=data.title,
                body=data.body,
                display_order=(
                    data.display_order
                ),
                is_visible=data.is_visible,
            )
        )

    def update_section(
        self,
        project_id: int,
        section_id: int,
        data: ProjectSectionUpdate,
    ):
        self.get_project(project_id)

        section = self.repository.get_section(
            section_id
        )

        if (
            section is None
            or section.project_id != project_id
        ):
            raise ResourceNotFoundError(
                "Project section not found"
            )

        changes = data.model_dump(
            exclude_unset=True
        )

        if "section_type" in changes:
            if changes["section_type"] is None:
                raise DomainValidationError(
                    "Section type cannot be null"
                )

            section_type = (
                changes["section_type"]
                .strip()
                .upper()
            )

            if (
                section_type
                not in self.SECTION_TYPES
            ):
                raise DomainValidationError(
                    "Invalid project section type"
                )

            section.section_type = (
                section_type
            )

        for field in (
            "title",
            "body",
            "display_order",
            "is_visible",
        ):
            if field in changes:
                setattr(
                    section,
                    field,
                    changes[field],
                )

        return self.repository.save_section(
            section
        )

    def delete_section(
        self,
        project_id: int,
        section_id: int,
    ):
        self.get_project(project_id)

        section = self.repository.get_section(
            section_id
        )

        if (
            section is None
            or section.project_id != project_id
        ):
            raise ResourceNotFoundError(
                "Project section not found"
            )

        self.repository.delete_section(
            section
        )

    # ITEMS

    def create_section_item(
        self,
        project_id: int,
        section_id: int,
        data: ProjectSectionItemCreate,
    ):
        self.get_project(project_id)

        section = self.repository.get_section(
            section_id
        )

        if (
            section is None
            or section.project_id != project_id
        ):
            raise ResourceNotFoundError(
                "Project section not found"
            )

        return (
            self.repository.save_section_item(
                ProjectSectionItem(
                    project_section_id=section_id,
                    content=data.content.strip(),
                    display_order=data.display_order,
                    is_visible=data.is_visible,
                )
            )
        )

    def update_section_item(
        self,
        project_id: int,
        section_id: int,
        item_id: int,
        data: ProjectSectionItemUpdate,
    ):
        self.get_project(project_id)

        item = (
            self.repository.get_section_item(
                item_id
            )
        )

        if (
            item is None
            or item.project_section_id != section_id
        ):
            raise ResourceNotFoundError(
                "Project section item not found"
            )

        changes = data.model_dump(
            exclude_unset=True
        )

        if "content" in changes:
            if changes["content"] is None:
                raise DomainValidationError(
                    "Content cannot be null"
                )

            item.content = (
                changes["content"].strip()
            )

        for field in (
            "display_order",
            "is_visible",
        ):
            if field in changes:
                setattr(
                    item,
                    field,
                    changes[field],
                )

        return (
            self.repository.save_section_item(
                item
            )
        )

    def delete_section_item(
        self,
        project_id: int,
        section_id: int,
        item_id: int,
    ):
        self.get_project(project_id)

        item = (
            self.repository.get_section_item(
                item_id
            )
        )

        if (
            item is None
            or item.project_section_id != section_id
        ):
            raise ResourceNotFoundError(
                "Project section item not found"
            )

        self.repository.delete_section_item(
            item
        )