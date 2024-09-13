from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="forbid",
        env_prefix="dac_"
    )
    listenbrainz_token: str
    spotify_client_id: str
    spotify_client_secret: str
