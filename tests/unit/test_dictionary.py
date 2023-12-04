"""Tests for the dictionary module."""


import pytest
import pytest_mock

from linguaweb_api.core import dictionary


@pytest.fixture(autouse=True)
def _clear_cache() -> None:
    """Clears the cache before each test."""
    dictionary.read_words.cache_clear()


def test_read_words(mocker: pytest_mock.MockFixture) -> None:
    """Tests if the words are correctly read from the dictionary file."""
    mocker.patch("pathlib.Path.open", mocker.mock_open(read_data="word1\nword2\nword3"))

    words = dictionary.read_words()

    assert words == ["word1", "word2", "word3"]


def test_read_words_cache(mocker: pytest_mock.MockFixture) -> None:
    """Tests if the read_words function is cached."""
    mock = mocker.patch("pathlib.Path.open", mocker.mock_open(read_data=""))

    dictionary.read_words()
    dictionary.read_words()

    mock.assert_called_once()


def test_read_words_returns_empty_list_when_file_is_empty(
    mocker: pytest_mock.MockFixture,
) -> None:
    """Tests if an empty list is returned when the file is empty."""
    mocker.patch("pathlib.Path.open", mocker.mock_open(read_data=""))

    words = dictionary.read_words()

    assert words == []
