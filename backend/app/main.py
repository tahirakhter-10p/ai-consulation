import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.appointment import router as appointment_router
from app.api.consultation import router as consultation_router
from app.api.dashboard import router as dashboard_router
from app.api.health import router as health_router
from app.api.recommendation import router as recommendation_router
from app.api.treatment import router as treatment_router
from app.core.config import get_settings
from app.core.constants import DEFAULT_API_MESSAGE
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging

settings = get_settings()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging(settings.log_level)
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description=DEFAULT_API_MESSAGE,
    debug=settings.debug,
    lifespan=lifespan,
    docs_url="/docs",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin).rstrip("/") for origin in settings.cors_origins],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
register_exception_handlers(app)


@app.middleware("http")
async def log_request(request: Request, call_next):
    """Log request completion without recording request or response bodies."""

    try:
        response = await call_next(request)
    except Exception:
        logger.exception("HTTP request failed: %s %s", request.method, request.url.path)
        raise
    logger.info(
        "HTTP request completed: %s %s %s",
        request.method,
        request.url.path,
        response.status_code,
    )
    return response


app.include_router(health_router)
app.include_router(dashboard_router, prefix=settings.api_v1_prefix)
app.include_router(consultation_router, prefix=settings.api_v1_prefix)
app.include_router(recommendation_router, prefix=settings.api_v1_prefix)
app.include_router(appointment_router, prefix=settings.api_v1_prefix)
app.include_router(treatment_router, prefix=settings.api_v1_prefix)
