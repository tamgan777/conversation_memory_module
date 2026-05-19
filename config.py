"""
Configuration settings for the Conversation Memory Module.
"""
import os
from typing import Optional

# Application settings
APP_NAME = "Conversation Memory Module"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "FastAPI service for storing and retrieving conversation context"

# Server settings
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", 8000))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Database settings
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./conversation_memory.db"
)

# API settings
API_PREFIX = "/api/v1"
DOCS_URL = "/docs"
OPENAPI_URL = "/openapi.json"

# CORS settings
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
CORS_CREDENTIALS = True
CORS_METHODS = ["*"]
CORS_HEADERS = ["*"]

# Pagination settings
DEFAULT_SKIP = 0
DEFAULT_LIMIT = 100
MAX_LIMIT = 1000

# Validation settings
MAX_SESSION_ID_LENGTH = 255
MAX_TAGS_LENGTH = 500
MAX_QUESTION_LENGTH = 5000
MAX_ANSWER_LENGTH = 10000

# Logging settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


class Settings:
    """
    Application settings management.
    """
    app_name: str = APP_NAME
    app_version: str = APP_VERSION
    app_description: str = APP_DESCRIPTION

    server_host: str = SERVER_HOST
    server_port: int = SERVER_PORT
    debug: bool = DEBUG

    database_url: str = DATABASE_URL

    cors_origins: list = CORS_ORIGINS
    cors_credentials: bool = CORS_CREDENTIALS
    cors_methods: list = CORS_METHODS
    cors_headers: list = CORS_HEADERS

    def get_database_url(self) -> str:
        """Get the database URL."""
        return self.database_url

    def is_sqlite(self) -> bool:
        """Check if using SQLite."""
        return "sqlite" in self.database_url.lower()

    def is_debug(self) -> bool:
        """Check if debug mode is enabled."""
        return self.debug


# Global settings instance
settings = Settings()
