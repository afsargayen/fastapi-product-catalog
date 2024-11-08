import os
from dotenv import load_dotenv
from typing import Annotated, Any, Literal
from pydantic_settings import BaseSettings, SettingsConfigDict  # type: ignore
from pydantic import (
    AnyUrl,
    BeforeValidator,
    HttpUrl,
    computed_field,
    model_validator,
)
from pydantic_core import MultiHostUrl

load_dotenv()


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="allow"
    )

    SECRET_KEY: str = os.getenv("SECRET_KEY")

    def __getattr__(self, name: str):
        return os.getenv(name)

    @computed_field
    @property
    def server_host(self) -> str:
        if self.ENVIRONMENT == "local":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> Any:
        return MultiHostUrl.build(
            scheme=self.MYSQL_SCHEME,
            username=self.MYSQL_USER,
            password=self.MYSQL_PASSWORD,
            host=self.MYSQL_SERVER,
            port=int(self.MYSQL_PORT),
            path=self.MYSQL_DATABASE,
        )


settings = Settings()