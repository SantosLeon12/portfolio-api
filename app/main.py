from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exception_handlers import (
    register_exception_handlers,
)
from fastapi.middleware.cors import (
    CORSMiddleware,
)

app = FastAPI(
    title=settings.app_name,
    debug=settings.app_debug,
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

@app.get("/")
def root():
    return {
        "name": settings.app_name,
        "environment": settings.app_env,
        "status": "running",
    }


app.include_router(
    api_router,
    prefix="/api/v1",
)