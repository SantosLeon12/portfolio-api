from sqlalchemy import (
    func,
    select,
)
from sqlalchemy.orm import (
    Session,
    selectinload,
    with_loader_criteria,
)

from app.models.media_asset import MediaAsset
from app.models.organization import Organization
from app.models.profile import Profile
from app.models.project import Project
from app.models.project_category import (
    ProjectCategory,
)
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
from app.models.technology import Technology


class ProjectRepository:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    # COMMON

    def get_profile(self):
        return self.db.scalar(
            select(Profile)
            .order_by(Profile.id.asc())
            .limit(1)
        )

    def get_organization(
        self,
        organization_id: int,
    ):
        return self.db.get(
            Organization,
            organization_id,
        )

    def get_technology(
        self,
        technology_id: int,
    ):
        return self.db.get(
            Technology,
            technology_id,
        )

    def get_media(
        self,
        media_asset_id: int,
    ):
        return self.db.get(
            MediaAsset,
            media_asset_id,
        )

    # CATEGORIES

    def get_categories(self):
        return list(
            self.db.scalars(
                select(ProjectCategory)
                .order_by(
                    ProjectCategory
                    .display_order.asc(),
                    ProjectCategory.name.asc(),
                )
            ).all()
        )

    def get_category(
        self,
        category_id: int,
    ):
        return self.db.get(
            ProjectCategory,
            category_id,
        )

    def get_category_by_name(
        self,
        name: str,
    ):
        return self.db.scalar(
            select(ProjectCategory).where(
                func.lower(
                    ProjectCategory.name
                )
                == name.lower()
            )
        )

    def get_category_by_slug(
        self,
        slug: str,
    ):
        return self.db.scalar(
            select(ProjectCategory).where(
                ProjectCategory.slug == slug
            )
        )

    def save_category(
        self,
        category: ProjectCategory,
    ):
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)

        return category

    def delete_category(
        self,
        category: ProjectCategory,
    ):
        self.db.delete(category)
        self.db.commit()

    def count_category_usage(
        self,
        category_id: int,
    ):
        return (
            self.db.scalar(
                select(func.count())
                .select_from(
                    ProjectCategoryRelation
                )
                .where(
                    ProjectCategoryRelation.category_id
                    == category_id
                )
            )
            or 0
        )

    # PROJECT OPTIONS

    def _options(
        self,
        public_only: bool = False,
    ):
        options = [
            selectinload(
                Project.organization
            ),
            selectinload(
                Project.categories
            ).selectinload(
                ProjectCategoryRelation.category
            ),
            (
                selectinload(
                    Project.technologies
                )
                .selectinload(
                    ProjectTechnology.technology
                )
                .selectinload(
                    Technology.category
                )
            ),
            selectinload(
                Project.links
            ),
            (
                selectinload(
                    Project.media
                )
                .selectinload(
                    ProjectMedia.media_asset
                )
            ),
            (
                selectinload(
                    Project.sections
                )
                .selectinload(
                    ProjectSection.items
                )
            ),
        ]

        if public_only:
            options.extend([
                with_loader_criteria(
                    ProjectLink,
                    ProjectLink.is_visible.is_(
                        True
                    ),
                    include_aliases=True,
                ),
                with_loader_criteria(
                    ProjectMedia,
                    ProjectMedia.is_visible.is_(
                        True
                    ),
                    include_aliases=True,
                ),
                with_loader_criteria(
                    ProjectSection,
                    ProjectSection.is_visible.is_(
                        True
                    ),
                    include_aliases=True,
                ),
                with_loader_criteria(
                    ProjectSectionItem,
                    ProjectSectionItem.is_visible.is_(
                        True
                    ),
                    include_aliases=True,
                ),
            ])

        return options

    def get_projects(
        self,
        profile_id: int,
        public_only: bool = False,
        featured: bool | None = None,
    ):
        statement = (
            select(Project)
            .options(
                *self._options(public_only)
            )
            .where(
                Project.profile_id
                == profile_id
            )
        )

        if public_only:
            statement = statement.where(
                Project.status == "PUBLISHED"
            )

        if featured is not None:
            statement = statement.where(
                Project.featured
                == featured
            )

        statement = statement.order_by(
            Project.display_order.asc(),
            Project.published_at.desc(),
            Project.id.desc(),
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get_project(
        self,
        project_id: int,
    ):
        return self.db.scalar(
            select(Project)
            .options(*self._options())
            .where(
                Project.id == project_id
            )
        )

    def get_by_slug(
        self,
        slug: str,
        public_only: bool = False,
    ):
        statement = (
            select(Project)
            .options(
                *self._options(public_only)
            )
            .where(
                Project.slug == slug
            )
        )

        if public_only:
            statement = statement.where(
                Project.status == "PUBLISHED"
            )

        return self.db.scalar(statement)

    def save_project(
        self,
        project: Project,
    ):
        self.db.add(project)
        self.db.commit()

        return self.get_project(
            project.id
        )

    def delete_project(
        self,
        project: Project,
    ):
        self.db.delete(project)
        self.db.commit()

    # CATEGORY RELATIONS

    def get_category_relation(
        self,
        project_id: int,
        category_id: int,
    ):
        return self.db.scalar(
            select(ProjectCategoryRelation)
            .where(
                ProjectCategoryRelation.project_id
                == project_id,
                ProjectCategoryRelation.category_id
                == category_id,
            )
        )

    def save_category_relation(
        self,
        item: ProjectCategoryRelation,
    ):
        self.db.add(item)
        self.db.commit()
        return item

    def delete_category_relation(
        self,
        item: ProjectCategoryRelation,
    ):
        self.db.delete(item)
        self.db.commit()

    # TECHNOLOGIES

    def get_project_technology(
        self,
        project_id: int,
        technology_id: int,
    ):
        return self.db.scalar(
            select(ProjectTechnology)
            .options(
                selectinload(
                    ProjectTechnology.technology
                ).selectinload(
                    Technology.category
                )
            )
            .where(
                ProjectTechnology.project_id
                == project_id,
                ProjectTechnology.technology_id
                == technology_id,
            )
        )

    def save_project_technology(
        self,
        item: ProjectTechnology,
    ):
        self.db.add(item)
        self.db.commit()

        return self.get_project_technology(
            item.project_id,
            item.technology_id,
        )

    def delete_project_technology(
        self,
        item: ProjectTechnology,
    ):
        self.db.delete(item)
        self.db.commit()

    # LINKS

    def get_link(
        self,
        link_id: int,
    ):
        return self.db.get(
            ProjectLink,
            link_id,
        )

    def get_link_by_url(
        self,
        project_id: int,
        url: str,
    ):
        return self.db.scalar(
            select(ProjectLink).where(
                ProjectLink.project_id
                == project_id,
                ProjectLink.url == url,
            )
        )

    def save_link(
        self,
        item: ProjectLink,
    ):
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete_link(
        self,
        item: ProjectLink,
    ):
        self.db.delete(item)
        self.db.commit()

    # MEDIA

    def get_project_media(
        self,
        project_media_id: int,
    ):
        return self.db.scalar(
            select(ProjectMedia)
            .options(
                selectinload(
                    ProjectMedia.media_asset
                )
            )
            .where(
                ProjectMedia.id
                == project_media_id
            )
        )

    def get_project_media_by_asset(
        self,
        project_id: int,
        media_asset_id: int,
    ):
        return self.db.scalar(
            select(ProjectMedia).where(
                ProjectMedia.project_id
                == project_id,
                ProjectMedia.media_asset_id
                == media_asset_id,
            )
        )

    def save_project_media(
        self,
        item: ProjectMedia,
    ):
        self.db.add(item)
        self.db.commit()

        return self.get_project_media(
            item.id
        )

    def delete_project_media(
        self,
        item: ProjectMedia,
    ):
        self.db.delete(item)
        self.db.commit()

    # SECTIONS

    def get_section(
        self,
        section_id: int,
    ):
        return self.db.scalar(
            select(ProjectSection)
            .options(
                selectinload(
                    ProjectSection.items
                )
            )
            .where(
                ProjectSection.id
                == section_id
            )
        )

    def save_section(
        self,
        item: ProjectSection,
    ):
        self.db.add(item)
        self.db.commit()

        return self.get_section(
            item.id
        )

    def delete_section(
        self,
        item: ProjectSection,
    ):
        self.db.delete(item)
        self.db.commit()

    # SECTION ITEMS

    def get_section_item(
        self,
        item_id: int,
    ):
        return self.db.get(
            ProjectSectionItem,
            item_id,
        )

    def save_section_item(
        self,
        item: ProjectSectionItem,
    ):
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete_section_item(
        self,
        item: ProjectSectionItem,
    ):
        self.db.delete(item)
        self.db.commit()