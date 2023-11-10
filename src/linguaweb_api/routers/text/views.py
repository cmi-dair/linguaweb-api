"""View definitions for the text router."""
import logging

import fastapi
from fastapi import status
from sqlalchemy import orm

from linguaweb_api.core import config
from linguaweb_api.microservices import sql
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
) -> schemas.WordDescription:
    """Returns the description of a random word.

    Args:
        session: The database session.
        gpt: The GPT model to use.
    """
    logger.debug("Getting word description.")
    text_task = await controller.get_text_task(session)
    logger.debug("Got word description.")
    return text_task


@router.get(
    "/synonyms",
    response_model=schemas.WordSynonyms,
    status_code=status.HTTP_200_OK,
    summary="Returns synonyms of a random word.",
    description="Returns synonyms of a random word.",
)
async def get_word_synonym(
    session: orm.Session = fastapi.Depends(sql.get_session),
) -> schemas.WordSynonyms:
    """Returns synonyms of a random word.

    Args:
        session: The database session.
    """
    logger.debug("Getting word synonym.")
    text_task = await controller.get_text_task(session)
    logger.debug("Got word synonym.")
    return text_task


@router.get(
    "/antonyms",
    response_model=schemas.WordAntonyms,
    status_code=status.HTTP_200_OK,
    summary="Returns antonyms of a random word.",
    description="Returns antonyms of a random word.",
)
async def get_word_antonym(
    session: orm.Session = fastapi.Depends(sql.get_session),
) -> schemas.WordAntonyms:
    """Returns antonyms of a random word.

    Args:
        session: The database session.
    """
    logger.debug("Getting word antonym.")
    text_task = await controller.get_text_task(session)
    logger.debug("Got word antonym.")
    return text_task


@router.get(
    "/jeopardy",
    response_model=schemas.WordJeopardy,
    status_code=status.HTTP_200_OK,
    summary="Returns a jeopardy question of a random word.",
    description="Returns a jeopardy question of a random word.",
)
async def get_word_jeopardy(
    session: orm.Session = fastapi.Depends(sql.get_session),
) -> schemas.WordJeopardy:
    """Returns a jeopardy question of a random word.

    Args:
        session: The database session.
    """
    logger.debug("Getting word jeopardy.")
    text_task = await controller.get_text_task(session)
    logger.debug("Got word jeopardy.")
    return text_task


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
    is_correct = await controller.check_word(word_id, checks, session)
    logger.debug("Checked word.")
    return is_correct
