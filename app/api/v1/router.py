from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.public.technologies import (
    router as technologies_router,
)
from app.api.v1.admin.technologies import (
    router as admin_technologies_router,
)
from app.api.v1.admin.technology_categories import (
    router as admin_technology_categories_router,
)
from app.api.v1.auth import router as auth_router
from app.api.v1.admin.profile import (
    router as admin_profile_router,
)
from app.api.v1.public.profile import (
    router as public_profile_router,
)
from app.api.v1.admin.organizations import (
    router as admin_organizations_router,
)
from app.api.v1.public.organizations import (
    router as public_organizations_router,
)
from app.api.v1.admin.languages import (
    router as admin_languages_router,
)
from app.api.v1.admin.professional import (
    router as admin_professional_router,
)
from app.api.v1.public.languages import (
    router as public_languages_router,
)
from app.api.v1.public.professional import (
    router as public_professional_router,
)
from app.api.v1.admin.contact_messages import (
    router as admin_contact_messages_router,
)
from app.api.v1.admin.media import (
    router as admin_media_router,
)
from app.api.v1.admin.profile_technologies import (
    router as admin_profile_technologies_router,
)
from app.api.v1.admin.project_categories import (
    router as admin_project_categories_router,
)
from app.api.v1.admin.projects import (
    router as admin_projects_router,
)

from app.api.v1.public.contact import (
    router as public_contact_router,
)
from app.api.v1.public.profile_technologies import (
    router as public_profile_technologies_router,
)
from app.api.v1.public.projects import (
    router as public_projects_router,
)
from app.api.v1.public.media import (
    router as public_media_router,
)

api_router = APIRouter()


api_router.include_router(
    health_router,
)

api_router.include_router(
    technologies_router,
    prefix="/public",
)
api_router.include_router(
    auth_router,
)
api_router.include_router(
    admin_technology_categories_router,
    prefix="/admin",
)

api_router.include_router(
    admin_technologies_router,
    prefix="/admin",
)
api_router.include_router(
    public_profile_router,
    prefix="/public",
)

api_router.include_router(
    admin_profile_router,
    prefix="/admin",
)

api_router.include_router(
    public_organizations_router,
    prefix="/public",
)
api_router.include_router(
    admin_organizations_router,
    prefix="/admin",
)
api_router.include_router(
    public_professional_router,
    prefix="/public",
)

api_router.include_router(
    public_languages_router,
    prefix="/public",
)

api_router.include_router(
    admin_professional_router,
    prefix="/admin",
)

api_router.include_router(
    admin_languages_router,
    prefix="/admin",
)

api_router.include_router(
    public_profile_technologies_router,
    prefix="/public",
)

api_router.include_router(
    public_projects_router,
    prefix="/public",
)

api_router.include_router(
    public_contact_router,
    prefix="/public",
)

api_router.include_router(
    admin_profile_technologies_router,
    prefix="/admin",
)

api_router.include_router(
    admin_media_router,
    prefix="/admin",
)

api_router.include_router(
    admin_project_categories_router,
    prefix="/admin",
)

api_router.include_router(
    admin_projects_router,
    prefix="/admin",
)

api_router.include_router(
    admin_contact_messages_router,
    prefix="/admin",
)

api_router.include_router(
    public_media_router,
    prefix="/public",
)
