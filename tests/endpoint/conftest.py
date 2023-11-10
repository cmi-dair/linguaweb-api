"""Fixtures and configurations for testing the endpoints of the CTK API."""
import enum

import pytest
import sqlalchemy
from fastapi import testclient
from sqlalchemy import orm

from linguaweb_api import main
from linguaweb_api.microservices import sql

API_ROOT = "/api/v1"


class Endpoints(str, enum.Enum):
    """Enum class that represents the available endpoints for the API."""

    GET_DESCRIPTION = f"{API_ROOT}/text/description"
    GET_SYNONYMS = f"{API_ROOT}/text/synonyms"
    GET_ANTONYMS = f"{API_ROOT}/text/antonyms"
    GET_JEOPARDY = f"{API_ROOT}/text/jeopardy"
    POST_CHECK_WORD = f"{API_ROOT}/text/check/{{word_id}}"
    GET_HEALTH = f"{API_ROOT}/health"


@pytest.fixture()
def endpoints() -> type[Endpoints]:
    """Returns the Endpoints enum class."""
    return Endpoints


@pytest.fixture()
def client() -> testclient.TestClient:
    """Returns a test client for the API."""
    return testclient.TestClient(main.app)


@pytest.fixture(autouse=True, scope="session")
def _start_database() -> None:
    """Starts the database."""
    main.database.create_database()


@pytest.fixture()
def session() -> orm.Session:
    """Returns a database session."""
    return next(sql.get_session())


@pytest.fixture(autouse=True)
def _clear_tables(session: orm.Session) -> None:
    """Clear all tables by deleting all their rows.

    Args:
        session: The database session.
    """
    base = orm.declarative_base()
    metadata = sqlalchemy.MetaData()
    metadata.reflect(bind=session.get_bind())
    base.metadata = metadata

    for table in reversed(metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()
