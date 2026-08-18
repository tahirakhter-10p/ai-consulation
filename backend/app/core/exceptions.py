import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


class ApplicationError(Exception):
    """Base exception for application-level failures."""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "An unexpected application error occurred."


class ResourceNotFoundError(ApplicationError):
    """Reserved for future resource lookup failures."""

    status_code = status.HTTP_404_NOT_FOUND
    detail = "The requested resource was not found."


class ConflictError(ApplicationError):
    """Raised when an operation would violate a domain uniqueness rule."""

    status_code = status.HTTP_409_CONFLICT
    detail = "The requested operation conflicts with the current resource state."


class InvalidOperationError(ApplicationError):
    """Raised when a service receives invalid domain input."""

    status_code = status.HTTP_400_BAD_REQUEST
    detail = "The requested operation is invalid."


class AIServiceError(ApplicationError):
    """Raised when an AI provider cannot produce a usable response."""

    status_code = status.HTTP_502_BAD_GATEWAY
    detail = "The AI service is currently unavailable."


def _error_response(
    status_code: int,
    message: str,
    errors: list[dict[str, str]] | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"success": False, "message": message, "errors": errors or []},
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Install central exception handling before domain APIs are introduced."""

    @app.exception_handler(ApplicationError)
    async def handle_application_error(_: Request, exc: ApplicationError) -> JSONResponse:
        return _error_response(exc.status_code, exc.detail)

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
        errors = [
            {
                "field": ".".join(
                    str(part) for part in error["loc"] if part not in {"body", "query", "path"}
                ),
                "message": error["msg"],
            }
            for error in exc.errors()
        ]
        return _error_response(status.HTTP_400_BAD_REQUEST, "Validation failed.", errors)

    @app.exception_handler(StarletteHTTPException)
    async def handle_http_error(_: Request, exc: StarletteHTTPException) -> JSONResponse:
        return _error_response(exc.status_code, str(exc.detail))

    @app.exception_handler(Exception)
    async def handle_unexpected_error(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled application error", exc_info=exc)
        return _error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error.")
