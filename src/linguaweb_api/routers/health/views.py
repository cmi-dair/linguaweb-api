"""View definitions for the health router."""
import logging

import fastapi

from linguaweb_api.core import config
from linguaweb_api.routers.health import controller

settings = config.get_settings()
LOGGER_NAME = settings.LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

router = fastapi.APIRouter(prefix="/health", tags=["health"])


@router.get(
    "",
    status_code=fastapi.status.HTTP_200_OK,
    summary="Returns the health of the API.",
    description=(
        "Returns the health of the API. This will always be an empty 200 "
        "response if the server is running, any other response is indicative of a "
        "serious issues."
    ),
)
async def get_health() -> None:
    """Returns the health of the API."""
    logger.debug("Checking health.")
    return await controller.get_api_health()
