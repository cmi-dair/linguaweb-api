"""Schemas for the Words router."""
import pydantic


class WordData(pydantic.BaseModel):
    """Word data, without the word itself."""

    id: int
    description: str
    synonyms: list[str]
    antonyms: list[str]
    jeopardy: str
    s3_key: str
