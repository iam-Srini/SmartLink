from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url : str 
    secret_key : str
    algorithm : str
    access_token_expiration_minutes : int
    #refresh_token_expiration_days : int

    class Config:
        env_file = ".env"

settings = Settings()