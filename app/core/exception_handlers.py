from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    DomainValidationError,
    ResourceConflictError,
    ResourceInUseError,
    ResourceNotFoundError,
)


def register_exception_handlers(
    app: FastAPI,
) -> None:

    @app.exception_handler(
        ResourceNotFoundError
    )
    async def handle_not_found(
        request: Request,
        exc: ResourceNotFoundError,
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "detail": exc.message,
            },
        )

    @app.exception_handler(
        ResourceConflictError
    )
    async def handle_conflict(
        request: Request,
        exc: ResourceConflictError,
    ):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "detail": exc.message,
            },
        )

    @app.exception_handler(
        ResourceInUseError
    )
    async def handle_in_use(
        request: Request,
        exc: ResourceInUseError,
    ):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "detail": exc.message,
            },
        )

    @app.exception_handler(
        DomainValidationError
    )
    async def handle_validation(
        request: Request,
        exc: DomainValidationError,
    ):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": exc.message,
            },
        )