from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables.
    """

    # Database and authentication
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expiration_minutes: int

    # Mail configuration
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    mail_starttls: bool
    mail_ssl_tls: bool
    use_credentials: bool = True
    validate_certs: bool = True

    model_config = ConfigDict(env_file=".env")


settings = Settings()
