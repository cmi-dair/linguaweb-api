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


@pytest.mark.parametrize(
    "endpoint_type",
    [
        "description",
        "synonyms",
        "antonyms",
        "jeopardy",
    ],
)
def test_get_text_entry_exist(
    mocker: pytest_mock.MockFixture,
    endpoint_type: str,
    text_task: text_model.TextTask,
    client: testclient.TestClient,
    endpoints: conftest.Endpoints,
) -> None:
    """Tests the get text task endpoints with an existing file."""
    mocker.patch(
        "linguaweb_api.core.dictionary.get_random_word",
        return_value=text_task.word,
    )
    endpoint = getattr(endpoints, f"GET_{endpoint_type.upper()}")

    response = client.get(endpoint)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == text_task.id
    if endpoint_type in ("synonyms", "antonyms"):
        assert response.json()[endpoint_type][0] == f"mock_{endpoint_type}"
    else:
        assert response.json()[endpoint_type] == f"mock_{endpoint_type}"


@pytest.mark.parametrize(
    "endpoint_type",
    [
        "description",
        "synonyms",
        "antonyms",
        "jeopardy",
    ],
)
def test_get_text_entry_does_not_exist(
    mocker: pytest_mock.MockFixture,
    endpoint_type: str,
    client: testclient.TestClient,
    endpoints: conftest.Endpoints,
) -> None:
    """Tests the get text task endpoints with no existing file."""
    mock_gpt = mocker.patch(
        "linguaweb_api.microservices.openai.GPT.run",
        return_value="mock",
    )
    expected_n_gpt_calls = 4
    endpoint = getattr(endpoints, f"GET_{endpoint_type.upper()}")

    response = client.get(endpoint)

    assert mock_gpt.call_count == expected_n_gpt_calls
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json()["id"], int)
    if endpoint_type in ("synonyms", "antonyms"):
        assert isinstance(response.json()[endpoint_type], list)
    else:
        assert isinstance(response.json()[endpoint_type], str)


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
