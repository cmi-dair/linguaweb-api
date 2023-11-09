"""Tests for the text endpoints."""
import pytest_mock
from fastapi import status, testclient

from tests.endpoint import conftest


def test_get_description_entry_does_not_exist(
    mocker: pytest_mock.MockFixture,
    client: testclient.TestClient,
    endpoints: conftest.Endpoints,
) -> None:
    """Tests the get health endpoint."""
    mocker.patch(
        "linguaweb_api.microservices.openai.GPT.run",
        return_value="mock_description",
    )

    response = client.get(endpoints.GET_DESCRIPTION)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["description"] == "mock_description"
    assert isinstance(response.json()["id"], int)


def test_get_description_entry_exist_without_description(
    mocker: pytest_mock.MockFixture,
    client: testclient.TestClient,
    endpoints: conftest.Endpoints,
) -> None:
    """Tests the get health endpoint."""
    mocker.patch(
        "linguaweb_api.microservices.openai.GPT.run",
        return_value="mock_description",
    )

    response = client.get(endpoints.GET_DESCRIPTION)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["description"] == "mock_description"
    assert isinstance(response.json()["id"], int)
