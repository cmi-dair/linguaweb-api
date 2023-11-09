"""View definitions for the text router."""
import logging

import fastapi
from sqlalchemy import orm

from linguaweb_api.core import config
from linguaweb_api.microservices import openai, sql
from linguaweb_api.routers.text import controller, schemas

settings = config.get_settings()
LOGGER_NAME = settings.LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

router = fastapi.APIRouter(prefix="/text", tags=["text"])


@router.get("/description")
async def get_word_description(
    session: orm.Session = fastapi.Depends(sql.get_session),
    gpt: openai.GPT = fastapi.Depends(openai.GPT),
) -> schemas.WordDescription:
    """Returns the description of a random word.

    Args:
        session: The database session.
        gpt: The GPT model to use.
    """
    logger.debug("Getting word description.")
    return await controller.get_word_description(session, gpt)
