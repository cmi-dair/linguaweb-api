"""This module contains interactions with OpenAI models."""
import logging
from typing import Literal, TypedDict

import openai

from linguaweb_api.core import config

settings = config.get_settings()
OPENAI_API_KEY = settings.OPENAI_API_KEY
LOGGER_NAME = settings.LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


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

    def run(self, *, prompt: str, system_prompt: str) -> str:
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
