from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    db_url: str = "postgresql+asyncpg://postgres:postgres@qr-db:5432/qr_db"


db_settings = DatabaseConfig()
