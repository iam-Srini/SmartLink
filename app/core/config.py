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
    mail_username: str = "test@test.com"
    mail_password: str = "password"
    mail_from: str = "test@test.com"
    mail_port: int = 587
    mail_server: str = "smtp.test.com"
    mail_starttls: bool = True
    mail_ssl_tls: bool = False
    use_credentials: bool = True
    validate_certs: bool = True

    model_config = ConfigDict(env_file=".env")


settings = Settings()
