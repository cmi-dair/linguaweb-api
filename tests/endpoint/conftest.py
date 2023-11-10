"""Fixtures and configurations for testing the endpoints of the CTK API."""
import enum

import pytest
from fastapi import testclient

from linguaweb_api import main

API_ROOT = "/api/v1"


class Endpoints(str, enum.Enum):
    """Enum class that represents the available endpoints for the API."""

    GET_HEALTH = f"{API_ROOT}/health"
    GET_DESCRIPTION = f"{API_ROOT}/text/description"


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
