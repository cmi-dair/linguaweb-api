"""Business logic for the text router."""
import logging

from sqlalchemy import orm

from linguaweb_api.core import config, dictionary
from linguaweb_api.microservices import openai
from linguaweb_api.routers.text import models

settings = config.get_settings()
LOGGER_NAME = settings.LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


async def get_word_description(
    session: orm.Session,
    gpt: openai.GPT,
) -> models.TextTask:
    """Returns the description of a random word.

    Args:
        session: The database session.
        gpt: The GPT model to use.

    Returns:
        The description of the word.

    """
    logger.debug("Checking description.")
    word = dictionary.get_random_word()

    word_database = session.query(models.TextTask).filter_by(word=word).first()
    if not word_database:
        logger.debug("Word not found in database.")
        word_database = models.TextTask(word=word)
        session.add(word_database)

    if word_database.description:
        logger.debug("Word description found in database.")
        return word_database

    logger.debug("Word description not found in database.")
    system_prompt = (
        "Return a brief definition for the word provided by the user without using the "
        "word (or number, if relevant) in the definition."
    )
    description = gpt.run(prompt=word, system_prompt=system_prompt)
    word_database.description = description
    session.commit()
    return word_database
