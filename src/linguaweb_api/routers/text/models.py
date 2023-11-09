"""Models for the text router."""
import sqlalchemy
from sqlalchemy import orm

from linguaweb_api.core import models


class TextTask(models.BaseTable):
    """Table for text tasks."""

    __tablename__ = "text_tasks"

    word: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(64), unique=True)
    description: orm.Mapped[str] = orm.mapped_column(
        sqlalchemy.String(1024),
        nullable=True,
    )
