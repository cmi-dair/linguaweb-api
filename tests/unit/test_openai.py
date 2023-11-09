"""Unit tests for the OpenAI microservice."""
# pylint: disable=redefined-outer-name
from unittest import mock

import pytest
import pytest_mock

from linguaweb_api.microservices import openai


@pytest.fixture()
def mock_openai_client(
    mocker: pytest_mock.MockerFixture,
) -> mock.MagicMock:
    """Fixture to mock the OpenAI client."""
    mock_client = mock.MagicMock()
    mock_client.chat.completions.create.return_value = {
        "choices": [{"message": {"content": "Mocked response"}}],
    }
    mocker.patch("openai.OpenAI", return_value=mock_client)
    return mock_client


@pytest.fixture()
def gpt_instance(
    mock_openai_client: mock.MagicMock,
) -> openai.GPT:
    """Fixture to create a GPT instance with a mocked OpenAI client."""
    return openai.GPT()


def test_gpt_run_method(
    gpt_instance: openai.GPT,
    mocker: pytest_mock.MockerFixture,
) -> None:
    """Test the GPT run method returns the correct response."""
    system_prompt = "Test system message"
    user_prompt = "Test user message"
    expected_response = "Mocked response"
    mocker.patch.object(
        gpt_instance.client,
        "chat.completions.create",
        return_value={
            "choices": [{"message": {"content": expected_response}}],
        },
    )

    actual_response = gpt_instance.run(prompt=user_prompt, system_prompt=system_prompt)

    gpt_instance.client.chat.completions.create.assert_called_once_with(  # type: ignore[attr-defined]
        model=gpt_instance.model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    assert (
        actual_response == expected_response
    ), "The run method should return the expected mocked response"
