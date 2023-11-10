"""Models for the text router."""
from typing import Any

import sqlalchemy
from sqlalchemy import orm, types

from linguaweb_api.core import models


class CommaSeparatedList(types.TypeDecorator):
    """A custom SQLAlchemy for comma separated lists."""

    impl = sqlalchemy.String(1024)

    def process_bind_param(self, value: Any | None, dialect: Any) -> str | None:  # noqa: ANN401, ARG002
        """Converts a list of strings to a comma separated string.

        Args:
            value: The list of strings or a comma separated string.
            dialect: The dialect.

        Returns:
            str | None: The comma separated string.
        """
        if value is None:
            return None
        if isinstance(value, list):
            return ",".join(value)
        return value

    def process_result_value(self, value: Any | None, dialect: Any) -> list[str] | None:  # noqa: ARG002, ANN401
        """Converts a comma separated string to a list of strings.

        Args:
            value: The comma separated string.
            dialect: The dialect.

        Returns:
            list[str]: The list of strings.
        """
        if value is None:
            return None
        return value.split(",")


class TextTask(models.BaseTable):
    """Table for text tasks."""

    __tablename__ = "text_tasks"

    word: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(64), unique=True)
    description: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(1024))
    synonyms: orm.Mapped[str] = orm.mapped_column(CommaSeparatedList)
    antonyms: orm.Mapped[str] = orm.mapped_column(CommaSeparatedList)
    jeopardy: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(1024))
