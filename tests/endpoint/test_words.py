"""Tests for the words endpoints."""
import moto
import pytest
import pytest_mock
from fastapi import status, testclient
from sqlalchemy import orm

from linguaweb_api.core import models
from tests.endpoint import conftest


@pytest.fixture()
def word(session: orm.Session) -> models.Word:
    """Inserts a listening task into the database.

    Args:
        session: The database session.
    """
    audio = models.Word(
        word="The bird",
        description="The description is the word.",
        synonyms=["The", "synonym", "is", "the", "word."],
        antonyms=["The", "antonym", "is", "the", "word."],
        jeopardy="The jeopardy is the word.",
        s3_key="mock_s3_key",
    )
    session.add(audio)
    session.commit()
    return audio


def test_get_all_word_ids(
    word: models.Word,
    client: testclient.TestClient,
    endpoints: conftest.Endpoints,
) -> None:
    """Tests the get all word IDs endpoint."""
    response = client.get(endpoints.GET_ALL_WORD_IDS)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [word.id]


def test_get_all_word_ids_empty(
    client: testclient.TestClient,
    endpoints: conftest.Endpoints,
) -> None:
    """Tests the get all word IDs endpoint when the database is empty."""
    response = client.get(endpoints.GET_ALL_WORD_IDS)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_word(
    word: models.Word,
    client: testclient.TestClient,
    endpoints: conftest.Endpoints,
) -> None:
    """Tests the get word info endpoint."""
    endpoint = endpoints.GET_WORD.format(word_id=word.id)

    response = client.get(endpoint)

    assert response.status_code == status.HTTP_200_OK
    assert all(item in word.__dict__.items() for item in response.json().items())


def test_get_word_does_not_exist(
    client: testclient.TestClient,
    endpoints: conftest.Endpoints,
) -> None:
    """Tests the get word info endpoint when the word does not exist."""
    endpoint = endpoints.GET_WORD.format(word_id=-1)

    response = client.get(endpoint)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_post_check_word(
    word: models.Word,
    client: testclient.TestClient,
    endpoints: conftest.Endpoints,
) -> None:
    """Tests the check word endpoint."""
    endpoint = endpoints.POST_CHECK_WORD.format(word_id=word.id)

    response = client.post(endpoint, data={"word": word.word})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() is True


def test_post_check_word_case_insensitive(
    word: models.Word,
    client: testclient.TestClient,
    endpoints: conftest.Endpoints,
) -> None:
    """Tests the check word endpoint with wrong case."""
    endpoint = endpoints.POST_CHECK_WORD.format(word_id=word.id)

    response = client.post(endpoint, data={"word": word.word.upper()})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() is True


def test_post_check_word_with_spaces(
    word: models.Word,
    client: testclient.TestClient,
    endpoints: conftest.Endpoints,
) -> None:
    """Tests the check word endpoint with leading and trailing spaces."""
    endpoint = endpoints.POST_CHECK_WORD.format(word_id=word.id)

    response = client.post(endpoint, data={"word": f" {word.word} \n"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() is True


@moto.mock_s3
def test_get_audio(
    mocker: pytest_mock.MockFixture,
    word: models.Word,
    client: testclient.TestClient,
    endpoints: conftest.Endpoints,
) -> None:
    """Tests the get audio endpoint."""
    mocker.patch(
        "linguaweb_api.microservices.s3.S3.read",
        return_value=b"mock_audio_bytes",
    )
    endpoint = endpoints.GET_AUDIO.format(audio_id=word.id)

    response = client.get(endpoint)

    assert response.status_code == status.HTTP_200_OK
    assert response.content == b"mock_audio_bytes"
