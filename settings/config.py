from pydantic import BaseSettings


class Settings(BaseSettings):
    db_url: str = "mongodb://localhost:27017/"
    db_name: str = "iam"

    class Config:
        env_file = ".env"


settings = Settings()
