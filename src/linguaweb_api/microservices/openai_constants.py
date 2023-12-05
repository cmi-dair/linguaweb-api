"""Settings for OpenAI.

These settings are kept in a separate file to avoid circular imports on
the openai and config modules.
"""
import enum


class Voices(str, enum.Enum):
    """A class representing the voices for the Text-To-Speech model."""

    ALLOY = "alloy"
    ECHO = "echo"
    FABLE = "fable"
    ONYX = "onyx"
    NOVA = "nova"
    SHIMMER = "shimmer"


class TTSModels(str, enum.Enum):
    """Supported Text-To-Speech models."""

    TTS1 = "tts-1"


class STTModels(str, enum.Enum):
    """Supported Speech-To-Text models."""

    WHISPER1 = "whisper-1"


class GPTModels(str, enum.Enum):
    """Supported GPT models."""

    GPT4_1106_Preview = "gpt-4-1106-preview"
    GPT4 = "gpt-4"

    GPT35_turbo_1106 = "gpt3-5-turbo-1106"
    GPT35_turbo = "gpt3-5-turbo"


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
