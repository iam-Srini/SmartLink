from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables.
    """

    # Database and authentication
    database_url: str = "sqlite:///./test.db"
    secret_key: str = "supersecretkey"
    algorithm: str = "HS256"
    access_token_expiration_minutes: int = 30

    # Mail configuration
    mail_password: str = "password"
    mail_from: str = "test@test.com"

    model_config = ConfigDict(env_file=".env")


settings = Settings()
