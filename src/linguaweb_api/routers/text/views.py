"""View definitions for the text router."""
import logging

import fastapi
from fastapi import status
from sqlalchemy import orm

from linguaweb_api.core import config
from linguaweb_api.microservices import openai, sql
from linguaweb_api.routers.text import controller, schemas

settings = config.get_settings()
LOGGER_NAME = settings.LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

router = fastapi.APIRouter(prefix="/text", tags=["text"])


@router.get(
    "/description",
    response_model=schemas.WordDescription,
    status_code=status.HTTP_200_OK,
    summary="Returns the description of a random word.",
    description="Returns the description of a random word.",
)
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


@router.post(
    "/check/{word_id}",
    response_model=bool,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "No checks provided.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Word not found.",
        },
    },
    summary="Checks whether a word was guessed correctly.",
    description="Takes a word ID and a word, and checks whether the word was guessed "
    "correctly.",
)
async def check_word(
    word_id: int = fastapi.Path(..., title="The ID of the word to check."),
    checks: schemas.WordCheck = fastapi.Body(..., title="The information to check."),
    session: orm.Session = fastapi.Depends(sql.get_session),
) -> bool:
    """Checks attributes of a word.

    Args:
        word_id: The ID of the word to check.
        checks: The information to check.
        session: The database session.
    """
    logger.debug("Checking word.")
    return await controller.check_word(word_id, checks, session)
