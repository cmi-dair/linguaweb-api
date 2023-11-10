"""Tests for the text endpoints."""
import pytest
import pytest_mock
from fastapi import status, testclient
from sqlalchemy import orm

from linguaweb_api.routers.text import models as text_model
from tests.endpoint import conftest


@pytest.fixture()
def text_task(session: orm.Session) -> text_model.TextTask:
    """Inserts a text task into the database.

    Args:
        session: The database session.
    """
    word = text_model.TextTask(
        word="test",
        description="mock_description",
        synonyms="mock_synonyms",
        antonyms="mock_antonyms",
        jeopardy="mock_jeopardy",
    )
    session.add(word)
    session.commit()
    return word


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


def test_check_word_exists(
    client: testclient.TestClient,
    endpoints: conftest.Endpoints,
    text_task: text_model.TextTask,
) -> None:
    """Tests the check word description endpoint."""
    response = client.post(
        endpoints.POST_CHECK_WORD.format(word_id=text_task.id),
        json={"word": "test", "description": "mock_description"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() is True


def test_check_word_no_checks(
    client: testclient.TestClient,
    endpoints: conftest.Endpoints,
) -> None:
    """Tests the check word description endpoint when no checks are provided."""
    response = client.post(
        endpoints.POST_CHECK_WORD.format(word_id=1),
        json={},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_check_word_does_not_exist(
    client: testclient.TestClient,
    endpoints: conftest.Endpoints,
) -> None:
    """Tests the check word description endpoint when the word does not exist."""
    response = client.post(
        endpoints.POST_CHECK_WORD.format(word_id=1),
        json={"word": "test"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
