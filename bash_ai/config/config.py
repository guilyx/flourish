"""Configuration management for bash.ai."""

import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    def __init__(self):
        # Google AI configuration
        self.google_api_key: str | None = os.getenv("GOOGLE_API_KEY")
        if not self.google_api_key:
            raise ValueError(
                "GOOGLE_API_KEY environment variable is required. "
                "Please set it in your .env file or export it."
            )

        self.google_genai_use_vertexai: str = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "FALSE")
        self.model: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

        # Agent configuration
        self.default_allowlist: list[str] = (
            os.getenv("DEFAULT_ALLOWLIST", "").split(",") if os.getenv("DEFAULT_ALLOWLIST") else []
        )
        self.default_blacklist: list[str] = (
            os.getenv("DEFAULT_BLACKLIST", "rm,dd,format,mkfs,chmod 777").split(",")
            if os.getenv("DEFAULT_BLACKLIST")
            else []
        )

        # Session configuration
        self.app_name: str = os.getenv("APP_NAME", "bash.ai")
        self.user_id: str = os.getenv("USER_ID", "user")
        self.session_id: str = os.getenv("SESSION_ID", "session")


# Global settings instance
_settings: Settings | None = None


def get_settings() -> Settings:
    """Get or create the global settings instance.

    Returns:
        Settings instance
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
