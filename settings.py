from os import getenv
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    KAFKA_BROKER_URL: str = getenv("KAFKA_BROKER_URL", "localhost:9092")

    class Config:
        env_file = ".env"

settings = Settings()