from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days
    
    # Email settings
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    EMAIL_SENDER: str
    EMAIL_PASSWORD: str
    ADMIN_EMAIL: str
    

    class Config:
        env_file = ".env"


settings = Settings()
