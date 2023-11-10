"""A module for interacting with the SQL database."""
import logging
from collections import abc
from typing import Any

import sqlalchemy
from sqlalchemy import orm, pool

from linguaweb_api.core import config

settings = config.get_settings()
LOGGER_NAME = settings.LOGGER_NAME
POSTGRES_HOST = settings.POSTGRES_HOST
POSTGRES_PORT = settings.POSTGRES_PORT
POSTGRES_USER = settings.POSTGRES_USER
POSTGRES_PASSWORD = settings.POSTGRES_PASSWORD
ENVIRONMENT = settings.ENVIRONMENT

logger = logging.getLogger(LOGGER_NAME)

Base = orm.declarative_base()


class Database:
    """A class representing a database connection."""

    def __init__(self) -> None:
        """Initializes a new instance of the Database class.

        The Database class provides a high-level interface for interacting with a
        PostgreSQL database.
        """
        logger.debug("Initializing database.")
        db_url = self.get_db_url()
        engine_args: dict[str, Any] = {}
        if ENVIRONMENT == "development":
            engine_args["connect_args"] = {"check_same_thread": False}
            engine_args["poolclass"] = pool.StaticPool

        self.engine = sqlalchemy.create_engine(db_url, **engine_args)
        self.session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine,
            ),
        )

    def create_database(self) -> None:
        """Creates the database schema."""
        logger.debug("Creating database schema.")
        Base.metadata.create_all(self.engine)

    @staticmethod
    def get_db_url() -> str:
        """Returns the database URL based on the current environment.

        If the environment is set to 'development', returns a SQLite URL.
        Otherwise, returns a PostgreSQL URL based on the environment variables.
        """
        if ENVIRONMENT == "development":
            return "sqlite:///linguaweb.db"
        return (
            "postgresql://"
            f"{POSTGRES_USER.get_secret_value()}:"
            f"{POSTGRES_PASSWORD.get_secret_value()}@"
            f"{POSTGRES_HOST}:{POSTGRES_PORT}/linguaweb"
        )


def get_session() -> abc.Generator[orm.Session, None, None]:
    """Returns a database instance.

    Used for dependency injection in FastAPI.

    Returns:
        orm.Session: A database session.
    """
    session = Database().session_factory()
    try:
        yield session
    finally:
        session.close()
