from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from app.api.dependencies.auth import (
    get_current_admin,
)
from app.api.dependencies.project import (
    get_project_service,
)
from app.models.admin_user import AdminUser
from app.schemas.project import (
    ProjectCreate,
    ProjectLinkCreate,
    ProjectLinkResponse,
    ProjectLinkUpdate,
    ProjectListResponse,
    ProjectMediaCreate,
    ProjectMediaResponse,
    ProjectMediaUpdate,
    ProjectResponse,
    ProjectSectionCreate,
    ProjectSectionItemCreate,
    ProjectSectionItemResponse,
    ProjectSectionItemUpdate,
    ProjectSectionResponse,
    ProjectSectionUpdate,
    ProjectTechnologyCreate,
    ProjectTechnologyResponse,
    ProjectTechnologyUpdate,
    ProjectUpdate,
)
from app.services.project_service import (
    ProjectService,
)


router = APIRouter(
    prefix="/projects",
    tags=["Admin - Projects"],
)


@router.get(
    "",
    response_model=ProjectListResponse,
)
def get_projects(
    service: ProjectService = Depends(
        get_project_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    items, total = service.get_projects()

    return ProjectListResponse(
        items=items,
        total=total,
    )


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
)
def get_project(
    project_id: int,
    service: ProjectService = Depends(
        get_project_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.get_project(
        project_id
    )


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    payload: ProjectCreate,
    service: ProjectService = Depends(
        get_project_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.create_project(
        payload
    )


@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
)
def update_project(
    project_id: int,
    payload: ProjectUpdate,
    service: ProjectService = Depends(
        get_project_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.update_project(
        project_id,
        payload,
    )


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project(
    project_id: int,
    service: ProjectService = Depends(
        get_project_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    service.delete_project(project_id)
    return Response(status_code=204)


# CATEGORY RELATIONS

@router.post(
    "/{project_id}/categories/{category_id}",
    response_model=ProjectResponse,
)
def add_category(
    project_id: int,
    category_id: int,
    service: ProjectService = Depends(
        get_project_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.add_category(
        project_id,
        category_id,
    )


@router.delete(
    "/{project_id}/categories/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_category(
    project_id: int,
    category_id: int,
    service: ProjectService = Depends(
        get_project_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    service.remove_category(
        project_id,
        category_id,
    )
    return Response(status_code=204)


# TECHNOLOGIES

@router.post(
    "/{project_id}/technologies",
    response_model=ProjectTechnologyResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_technology(
    project_id: int,
    payload: ProjectTechnologyCreate,
    service: ProjectService = Depends(
        get_project_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.add_technology(
        project_id,
        payload,
    )


@router.patch(
    "/{project_id}/technologies/{technology_id}",
    response_model=ProjectTechnologyResponse,
)
def update_technology(
    project_id: int,
    technology_id: int,
    payload: ProjectTechnologyUpdate,
    service: ProjectService = Depends(
        get_project_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.update_technology(
        project_id,
        technology_id,
        payload,
    )


@router.delete(
    "/{project_id}/technologies/{technology_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_technology(
    project_id: int,
    technology_id: int,
    service: ProjectService = Depends(
        get_project_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    service.remove_technology(
        project_id,
        technology_id,
    )
    return Response(status_code=204)


# LINKS

@router.post(
    "/{project_id}/links",
    response_model=ProjectLinkResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_link(
    project_id: int,
    payload: ProjectLinkCreate,
    service: ProjectService = Depends(
        get_project_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.create_link(
        project_id,
        payload,
    )


@router.patch(
    "/{project_id}/links/{link_id}",
    response_model=ProjectLinkResponse,
)
def update_link(
    project_id: int,
    link_id: int,
    payload: ProjectLinkUpdate,
    service: ProjectService = Depends(
        get_project_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.update_link(
        project_id,
        link_id,
        payload,
    )


@router.delete(
    "/{project_id}/links/{link_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_link(
    project_id: int,
    link_id: int,
    service: ProjectService = Depends(
        get_project_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    service.delete_link(
        project_id,
        link_id,
    )
    return Response(status_code=204)


# MEDIA

@router.post(
    "/{project_id}/media",
    response_model=ProjectMediaResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_media(
    project_id: int,
    payload: ProjectMediaCreate,
    service: ProjectService = Depends(
        get_project_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.create_media(
        project_id,
        payload,
    )


@router.patch(
    "/{project_id}/media/{project_media_id}",
    response_model=ProjectMediaResponse,
)
def update_media(
    project_id: int,
    project_media_id: int,
    payload: ProjectMediaUpdate,
    service: ProjectService = Depends(
        get_project_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.update_media(
        project_id,
        project_media_id,
        payload,
    )


@router.delete(
    "/{project_id}/media/{project_media_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_media(
    project_id: int,
    project_media_id: int,
    service: ProjectService = Depends(
        get_project_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    service.delete_media(
        project_id,
        project_media_id,
    )
    return Response(status_code=204)


# SECTIONS

@router.post(
    "/{project_id}/sections",
    response_model=ProjectSectionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_section(
    project_id: int,
    payload: ProjectSectionCreate,
    service: ProjectService = Depends(
        get_project_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.create_section(
        project_id,
        payload,
    )


@router.patch(
    "/{project_id}/sections/{section_id}",
    response_model=ProjectSectionResponse,
)
def update_section(
    project_id: int,
    section_id: int,
    payload: ProjectSectionUpdate,
    service: ProjectService = Depends(
        get_project_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.update_section(
        project_id,
        section_id,
        payload,
    )


@router.delete(
    "/{project_id}/sections/{section_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_section(
    project_id: int,
    section_id: int,
    service: ProjectService = Depends(
        get_project_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    service.delete_section(
        project_id,
        section_id,
    )
    return Response(status_code=204)


# SECTION ITEMS

@router.post(
    "/{project_id}/sections/{section_id}/items",
    response_model=ProjectSectionItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_section_item(
    project_id: int,
    section_id: int,
    payload: ProjectSectionItemCreate,
    service: ProjectService = Depends(
        get_project_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.create_section_item(
        project_id,
        section_id,
        payload,
    )


@router.patch(
    "/{project_id}/sections/{section_id}/items/{item_id}",
    response_model=ProjectSectionItemResponse,
)
def update_section_item(
    project_id: int,
    section_id: int,
    item_id: int,
    payload: ProjectSectionItemUpdate,
    service: ProjectService = Depends(
        get_project_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return service.update_section_item(
        project_id,
        section_id,
        item_id,
        payload,
    )


@router.delete(
    "/{project_id}/sections/{section_id}/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_section_item(
    project_id: int,
    section_id: int,
    item_id: int,
    service: ProjectService = Depends(
        get_project_service
    ),
    _admin: AdminUser = Depends(
        get_current_admin
    ),
):
    service.delete_section_item(
        project_id,
        section_id,
        item_id,
    )
    return Response(status_code=204)