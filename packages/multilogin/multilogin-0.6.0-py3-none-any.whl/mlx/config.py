import logging
from typing import Tuple, Type

from pydantic import (
    Field,
    field_validator,
    model_validator,
    root_validator,
)
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)


from mlx.models import Credentials


class CredentialsConfig(Credentials, BaseSettings):
    model_config = SettingsConfigDict(
        # loc_by_alias=True,
        extra="allow",
    )

    @model_validator(mode="before")
    def check_token_or_credentials(cls, values):
        token = values.get("MLX_TOKEN")
        username = values.get("MLX_USERNAME")
        password = values.get("MLX_PASSWORD")

        if token:
            # If token is provided, bypass username and password validation
            values["MLX_USERNAME"] = values.get("MLX_USERNAME", "")
            values["MLX_PASSWORD"] = values.get("MLX_PASSWORD", "")
        elif not username or not password:
            raise ValueError(
                "Either MLX_TOKEN or both MLX_USERNAME and MLX_PASSWORD must be provided."
            )

        return values

    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (env_settings, init_settings, dotenv_settings, file_secret_settings)

    # model_config = SettingsConfigDict(
    #     env_file_encoding="utf-8",
    #     case_sensitive=False,
    #     frozen=False,
    #     extra="ignore",
    #     validate_all=False,
    # )

    def as_model(self):
        return Credentials(**self.dict())


from mlx.models import Profile


class LauncherConfig(BaseSettings):
    """
    Launcher config initializes with either the default profile and extra settings passed as JSON
    """

    body: dict = Field(alias="MLX_BODY", default=Profile.__default__)

    @field_validator("body")
    def validate_body(cls, v):
        return Profile.with_defaults(v)

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        case_sensitive=False,
        frozen=True,
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (env_settings,)


class EndpointsConfig(BaseSettings):
    launcher_v2: str = Field(default="https://launcher.mlx.yt:45001/api/v2")
    launcher_v1: str = Field(default="https://launcher.mlx.yt:45001/api/v1")
    multilogin: str = Field(default="https://api.multilogin.com")


class Config(EndpointsConfig):
    DEBUG: bool = Field(default=False, alias="DEBUG")
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return env_settings, file_secret_settings, dotenv_settings


# DEBUG = bool(os.getenv("DEBUG", False))


config = Config()

logging.debug(config)
