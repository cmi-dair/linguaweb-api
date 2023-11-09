"""Settings for the API."""
import functools
import logging

import pydantic
import pydantic_settings


class Settings(pydantic_settings.BaseSettings):  # type: ignore[valid-type, misc]
    """Settings for the API."""

    LOGGER_NAME: str = pydantic.Field("LinguaWeb API")
    LOGGER_VERBOSITY: int | None = pydantic.Field(
        logging.DEBUG,
        json_schema_extra={"env": "LOGGER_VERBOSITY"},
    )

    ENVIRONMENT: str = pydantic.Field(
        "development",
        json_schema_extra={"env": "ENVIRONMENT"},
    )

    OPENAI_API_KEY: pydantic.SecretStr = pydantic.Field(
        ...,
        json_schema_extra={"env": "OPENAI_API_KEY"},
    )

    POSTGRES_HOST: str = pydantic.Field(
        "localhost",
        json_schema_extra={"env": "POSTGRES_HOST"},
    )
    POSTGRES_PORT: int = pydantic.Field(
        5432,
        json_schema_extra={"env": "POSTGRES_PORT"},
    )
    POSTGRES_USER: pydantic.SecretStr = pydantic.Field(
        "postgres",
        json_schema_extra={"env": "POSTGRES_USER"},
    )
    POSTGRES_PASSWORD: pydantic.SecretStr = pydantic.Field(
        "postgres",
        json_schema_extra={"env": "POSTGRES_PASSWORD"},
    )

    MINIO_HOST: str = pydantic.Field(
        "localhost",
        json_schema_extra={"env": "MINIO_HOST"},
    )
    MINIO_PORT: int = pydantic.Field(
        9000,
        json_schema_extra={"env": "MINIO_PORT"},
    )
    MINIO_ROOT_USER: pydantic.SecretStr = pydantic.Field(
        ...,
        json_schema_extra={"env": "MINIO_ROOT_USER"},
    )
    MINIO_ROOT_PASSWORD: pydantic.SecretStr = pydantic.Field(
        ...,
        json_schema_extra={"env": "MINIO_ROOT_PASSWORD"},
    )
    MINIO_BUCKET: str = pydantic.Field(
        "linguaweb",
        json_schema_extra={"env": "MINIO_BUCKET"},
    )


@functools.lru_cache
def get_settings() -> Settings:
    """Cached fetcher for the API settings.

    Returns:
        The settings for the API.
    """
    return Settings()  # type: ignore[call-arg]


def initialize_logger() -> None:
    """Initializes the logger for the API."""
    settings = get_settings()
    logger = logging.getLogger(settings.LOGGER_NAME)
    if settings.LOGGER_VERBOSITY is not None:
        logger.setLevel(settings.LOGGER_VERBOSITY)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)s - %(funcName)s - %(message)s",  # noqa: E501
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
