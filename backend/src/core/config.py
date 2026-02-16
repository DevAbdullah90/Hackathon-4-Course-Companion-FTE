import boto3
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # Default to SQLite for local dev if Postgres not set
    DATABASE_URL: str = "sqlite:///./course.db"
    
    # Storage Configuration
    STORAGE_TYPE: str = "local" # Options: "local", "r2", "db"
    LOCAL_STORAGE_PATH: str = "./local_content"
    
    # Cloudflare R2 Configuration (Optional if STORAGE_TYPE=local)
    R2_ENDPOINT_URL: str = "https://example.r2.cloudflarestorage.com"
    R2_ACCESS_KEY_ID: str = "change_me"
    R2_SECRET_ACCESS_KEY: str = "change_me"
    R2_BUCKET_NAME: str = "course-content"
    
    # Authentication
    SECRET_KEY: str = "your-secret-key-here" # Change in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    API_V1_STR: str = "/api/v1"
    
    # AI Configuration
    GEMINI_API_KEY: str = "dummy-key" # Will be overridden by env var

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore" # Ignore extra env vars

settings = Settings()


def get_r2_client():
    if settings.STORAGE_TYPE == "local":
        return None
    return boto3.client(
        "s3",
        endpoint_url=settings.R2_ENDPOINT_URL,
        aws_access_key_id=settings.R2_ACCESS_KEY_ID,
        aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
    )
