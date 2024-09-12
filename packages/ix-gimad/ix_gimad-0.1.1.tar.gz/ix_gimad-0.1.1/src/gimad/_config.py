from pydantic_settings import (
    BaseSettings,
    JsonConfigSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
    YamlConfigSettingsSource,
)

from gimad._utils import CONFIG_NAME


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="GIMAD_",
        json_file=f"{CONFIG_NAME}.json",
        yaml_file=f"{CONFIG_NAME}.yaml",
        toml_file=f"{CONFIG_NAME}.toml",
    )

    db_url: str

    @classmethod
    def settings_customise_sources(  # noqa: PLR0913
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            env_settings,
            JsonConfigSettingsSource(settings_cls),
            TomlConfigSettingsSource(settings_cls),
            YamlConfigSettingsSource(settings_cls),
            init_settings,
        )


def load_config() -> Config:
    return Config()  # type:ignore
