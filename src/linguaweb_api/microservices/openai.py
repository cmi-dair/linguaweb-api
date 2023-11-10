"""This module contains interactions with OpenAI models."""
import enum
import logging
from typing import Literal, TypedDict

import openai

from linguaweb_api.core import config

settings = config.get_settings()
OPENAI_API_KEY = settings.OPENAI_API_KEY
LOGGER_NAME = settings.LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


class Prompts(str, enum.Enum):
    """A class representing the prompts for the GPT model."""

    WORD_DESCRIPTION = (
        "Return a brief definition for the word provided by the user without using the "
        "word (or number, if relevant) in the definition."
    )
    WORD_SYNONYMS = (
        "List synonyms for the following word without using the word (or "
        "number, if relevant) at all as a comma separated list"
    )
    WORD_ANTONYMS = (
        "List antonyms for the following word without using the word (or number, if "
        "relevant) at all as a comma separated list"
    )
    WORD_JEOPARDY = (
        "Return a very brief Jeopardy!-style description related to the following word "
        "without using the word (or number, if relevant) at all"
    )


class Message(TypedDict):
    """A message object."""

    role: Literal["system", "user"]
    content: str


class GPT:
    """A class representing the GPT model.

    Attributes:
        model: The name of the GPT model to use.
        client: The OpenAI client used to interact with the GPT model.
    """

    def __init__(self, model: str = "gpt-4-1106-preview") -> None:
        """Initializes a GPT object with the specified model.

        Args:
            model: The name of the GPT model to use. Defaults to
                "gpt-4-1106-preview".
        """
        self.model = model
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY.get_secret_value())

    async def run(self, *, prompt: str, system_prompt: str) -> str:
        """Runs the GPT model.

        Args:
            prompt: The prompt to run the model on.
            system_prompt: The system prompt to run the model on.

        Returns:
            The model's response.
        """
        messages = [
            Message(role="system", content=system_prompt),
            Message(role="user", content=prompt),
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,  # type: ignore[arg-type]
        )

        return response["choices"][0]["message"]["content"]  # type: ignore[index]
