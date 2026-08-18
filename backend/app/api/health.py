from fastapi import APIRouter, status

from app.api.responses import success_response
from app.core.constants import HEALTH_CHECK_PATH
from app.schemas.common import APIResponse

router = APIRouter(tags=["health"])


@router.get(HEALTH_CHECK_PATH, status_code=status.HTTP_200_OK, summary="Application health check")
async def health_check() -> APIResponse[dict[str, str]]:
    """Return process health without requiring a database connection."""

    return success_response(message="Application is healthy.", data={"status": "ok"})
