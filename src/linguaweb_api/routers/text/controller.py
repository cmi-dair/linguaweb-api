"""Business logic for the text router."""
import asyncio
import logging

import fastapi
from fastapi import status
from sqlalchemy import orm

from linguaweb_api.core import config, dictionary
from linguaweb_api.microservices import openai
from linguaweb_api.routers.text import models, schemas

settings = config.get_settings()
LOGGER_NAME = settings.LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


async def get_text_task(session: orm.Session) -> models.TextTask:
    """Returns the description of a random word.

    Args:
        session: The database session.

    Returns:
        The description of the word.

    """
    logger.debug("Checking description.")
    word = dictionary.get_random_word()

    if text_task := session.query(models.TextTask).filter_by(word=word).first():
        logger.debug("Text task already exists in database.")
        return text_task

    logger.debug("Running GPT.")
    gpt = openai.GPT()
    gpt_calls = [
        gpt.run(prompt=word, system_prompt=openai.Prompts.WORD_DESCRIPTION),
        gpt.run(prompt=word, system_prompt=openai.Prompts.WORD_SYNONYMS),
        gpt.run(prompt=word, system_prompt=openai.Prompts.WORD_ANTONYMS),
        gpt.run(prompt=word, system_prompt=openai.Prompts.WORD_JEOPARDY),
    ]
    results = await asyncio.gather(*gpt_calls)

    logger.debug("Creating new text task.")
    new_text_task = models.TextTask(
        word=word,
        description=results[0],
        synonyms=results[1],
        antonyms=results[2],
        jeopardy=results[3],
    )
    session.add(new_text_task)
    session.commit()
    logger.debug(new_text_task.id)
    return new_text_task


async def check_word(
    word_id: int,
    checks: schemas.WordCheck,
    session: orm.Session,
) -> bool:
    """Checks whether a word was guessed correctly.

    Args:
        word_id: The ID of the word to check.
        checks: The attributes to check.
        session: The database session.

    Returns:
        bool: Whether the word was guessed correctly.

    Raises:
        fastapi.HTTPException: 400 If no checks were provided.
        fastapi.HTTPException: 404 If the word was not found in the database.

    """
    logger.debug("Checking word description.")
    if not any(checks.model_dump().values()):
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="No checks provided.",
        )
    word_database = session.query(models.TextTask).filter_by(id=word_id).first()
    if not word_database:
        logger.warning("Word not found in database.")
        raise fastapi.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Word not found.",
        )

    for field, value in checks.model_dump().items():
        if value is not None and getattr(word_database, field) != value:
            return False
    return True
