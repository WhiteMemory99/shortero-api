from pydantic import BaseSettings


class Settings(BaseSettings):
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str
    postgres_password: str
    postgres_db: str

    def get_database_uri(self) -> str:
        password = f":{self.postgres_password}" if self.postgres_password else ""
        return "postgresql+asyncpg://{}{}@{}:{}/{}".format(
            self.postgres_user, password, self.postgres_host, self.postgres_port, self.postgres_db
        )

    class Config:
        env_file = ".env"


settings = Settings()
