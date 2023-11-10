"""Schemas returned from the API for the text tasks."""
import pydantic


class WordDescription(pydantic.BaseModel):
    """Word description task."""

    id: int
    description: str


class WordSynonyms(pydantic.BaseModel):
    """Word synonym task."""

    id: int
    synonyms: list[str]


class WordAntonyms(pydantic.BaseModel):
    """Word antonym task."""

    id: int
    antonyms: list[str]


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
