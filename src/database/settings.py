from dotenv import load_dotenv
from pydantic import root_validator
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """DB settings."""

    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    MONGO_HOST: str
    MONGO_PORT: int

    @root_validator(pre=False, skip_on_failure=True)
    def get_mongodb_uri(cls, values) -> dict:
        """Generate Mongo URI using env variables."""
        values["MONGO_URI"] = (
            f'mongodb://{values["MONGO_INITDB_ROOT_USERNAME"]}:{values["MONGO_INITDB_ROOT_PASSWORD"]}'
            f'@{values["MONGO_HOST"]}:{values["MONGO_PORT"]}'
        )

        return values

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
