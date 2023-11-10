"""Schemas returned from the API for the text tasks."""
import pydantic


class WordDescription(pydantic.BaseModel):
    """Word description task."""

    id: int
    description: str


class WordCheck(pydantic.BaseModel):
    """Schema for checking information about a word."""

    word: str | None = pydantic.Field(None, description="The target word.")
    description: str | None = pydantic.Field(
        None,
        description="The description of the word.",
    )
