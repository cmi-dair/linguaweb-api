"""Schemas returned from the API for the text tasks."""
import pydantic


class WordDescription(pydantic.BaseModel):
    """Word description task."""

    id: int
    description: str
