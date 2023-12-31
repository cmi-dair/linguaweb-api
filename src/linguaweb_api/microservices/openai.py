"""This module contains interactions with OpenAI models."""
import abc
import logging
import pathlib
from typing import Any, Literal, TypedDict

import fastapi
import openai
from fastapi import status

from linguaweb_api.core import config

settings = config.get_settings()
OPENAI_API_KEY = settings.OPENAI_API_KEY
OPENAI_GPT_MODEL = settings.OPENAI_GPT_MODEL
OPENAI_TTS_MODEL = settings.OPENAI_TTS_MODEL
OPENAI_STT_MODEL = settings.OPENAI_STT_MODEL
OPENAI_VOICE = settings.OPENAI_VOICE
LOGGER_NAME = settings.LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


class Message(TypedDict):
    """A message object."""

    role: Literal["system", "user"]
    content: str


class OpenAIBaseClass(abc.ABC):
    """An abstract base class for OpenAI models.

    This class initializes the OpenAI client.

    Attributes:
        client: The OpenAI client used to interact with the model.
    """

    def __init__(self) -> None:
        """Initializes a new instance of the OpenAIBaseClass class."""
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY.get_secret_value())

    @abc.abstractmethod
    def run(self, *_args: Any, **_kwargs: Any) -> Any:  # noqa: ANN401
        """Runs the model."""
        ...


class GPT(OpenAIBaseClass):
    """A class for running the GPT models."""

    async def run(
        self,
        *,
        prompt: str,
        system_prompt: str,
    ) -> str:
        """Runs the GPT model.

        Args:
            prompt: The prompt to run the model on.
            system_prompt: The system prompt to run the model on.
            model: The name of the GPT model to use.

        Returns:
            The model's response.
        """
        messages = [
            Message(role="system", content=system_prompt),
            Message(role="user", content=prompt),
        ]

        response = self.client.chat.completions.create(
            model=OPENAI_GPT_MODEL,
            messages=messages,  # type: ignore[arg-type]
        )

        if not response.choices[0].message.content:
            raise fastapi.HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Faulty response from OpenAI.",
            )
        return response.choices[0].message.content


class TextToSpeech(OpenAIBaseClass):
    """A class for running the Text-To-Speech models."""

    async def run(self, text: str) -> bytes:
        """Runs the Text-To-Speech model.

        Args:
            text: The text to convert to speech.
            model: The name of the Text-To-Speech model to use.

        Returns:
            The model's response.
        """
        response = self.client.audio.speech.create(
            model=OPENAI_TTS_MODEL.value,
            voice=OPENAI_VOICE.value,
            input=text,
        )

        return b"".join(response.iter_bytes())


class SpeechToText(OpenAIBaseClass):
    """A class for running the Speech-To-Text models."""

    async def run(self, audio_file: pathlib.Path | str) -> str:
        """Runs the Speech-To-Text model.

        Args:
            audio_file: The audio to convert to text.
            model: The name of the Speech-To-Text model to use.

        Returns:
            The model's response.
        """
        with pathlib.Path(audio_file).open("rb") as audio:
            return self.client.audio.transcriptions.create(
                model=OPENAI_STT_MODEL.value,
                file=audio,
                response_format="text",
            )  # type: ignore[return-value] # response_format overrides output type.
