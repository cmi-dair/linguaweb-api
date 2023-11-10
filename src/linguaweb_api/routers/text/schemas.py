"""Schemas returned from the API for the text tasks."""
import pydantic


class WordDescription(pydantic.BaseModel):
    """Word description task."""

    id: int
    description: str


class WordSynonym(pydantic.BaseModel):
    """Word synonym task."""

    id: int
    synonyms: str


class WordAntonym(pydantic.BaseModel):
    """Word antonym task."""

    id: int
    antonyms: str


class WordJeopardy(pydantic.BaseModel):
    """Word jeopardy task."""

    id: int
    jeopardy: str


class WordCheck(pydantic.BaseModel):
    """Schema for checking information about a word."""

    word: str | None = pydantic.Field(None, description="The target word.")
    description: str | None = pydantic.Field(
        None,
        description="The description of the word.",
    )
