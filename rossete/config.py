"""
Configuration management for Rossete.

Handles loading environment variables and providing typed configuration.
"""

from pathlib import Path
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

from .constants import (
    DEFAULT_EXPORT_FORMAT,
    DEFAULT_GROQ_MODEL,
    DEFAULT_LOG_LEVEL,
    DEFAULT_MAX_BLOCKS_PER_DOCUMENT,
    DEFAULT_MAX_CONCURRENT_REQUESTS,
    DEFAULT_MAX_TOKENS_PER_BLOCK,
    DEFAULT_STORAGE_PATH,
    DEFAULT_TEMPLATES_PATH,
    GROQ_MAX_RETRIES,
    GROQ_TIMEOUT,
)
from .exceptions import MissingEnvironmentVariableError


class Config(BaseSettings):
    """Application configuration from environment variables."""

    # Required Configuration
    groq_api_key: str = Field(
        ..., description="Groq API key for accessing LLM services"
    )

    # Groq Configuration
    groq_model: str = Field(
        default=DEFAULT_GROQ_MODEL, description="Groq model to use for generation"
    )
    groq_timeout: int = Field(
        default=GROQ_TIMEOUT, description="Timeout for Groq API calls in seconds"
    )
    groq_max_retries: int = Field(
        default=GROQ_MAX_RETRIES, description="Maximum number of retries for Groq API"
    )

    # Storage Configuration
    storage_path: str = Field(
        default=DEFAULT_STORAGE_PATH, description="Path for storing generated documents"
    )
    templates_path: str = Field(
        default=DEFAULT_TEMPLATES_PATH, description="Path to template definitions"
    )

    # Logging Configuration
    log_level: str = Field(
        default=DEFAULT_LOG_LEVEL, description="Logging level (DEBUG, INFO, WARNING, ERROR)"
    )

    # Concurrency Configuration
    max_concurrent_requests: int = Field(
        default=DEFAULT_MAX_CONCURRENT_REQUESTS,
        description="Maximum number of concurrent requests",
    )

    # Document Generation Limits
    max_blocks_per_document: int = Field(
        default=DEFAULT_MAX_BLOCKS_PER_DOCUMENT,
        description="Maximum blocks allowed per document",
    )
    max_tokens_per_block: int = Field(
        default=DEFAULT_MAX_TOKENS_PER_BLOCK,
        description="Maximum tokens allowed per block",
    )

    # Default Export Format
    default_export_format: str = Field(
        default=DEFAULT_EXPORT_FORMAT, description="Default export format"
    )

    model_config = {
        "env_prefix": "ROSSETE_",
        "case_sensitive": False,
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of {valid_levels}")
        return v.upper()

    @field_validator("max_concurrent_requests")
    @classmethod
    def validate_max_concurrent(cls, v: int) -> int:
        """Validate max concurrent requests."""
        if v < 1:
            raise ValueError("max_concurrent_requests must be at least 1")
        return v

    @field_validator("max_blocks_per_document")
    @classmethod
    def validate_max_blocks(cls, v: int) -> int:
        """Validate max blocks per document."""
        if v < 1:
            raise ValueError("max_blocks_per_document must be at least 1")
        return v

    @field_validator("max_tokens_per_block")
    @classmethod
    def validate_max_tokens(cls, v: int) -> int:
        """Validate max tokens per block."""
        if v < 100:
            raise ValueError("max_tokens_per_block must be at least 100")
        return v

    def get_storage_path(self) -> Path:
        """Get storage path as Path object."""
        path = Path(self.storage_path).expanduser().resolve()
        return path

    def get_templates_path(self) -> Path:
        """Get templates path as Path object."""
        path = Path(self.templates_path).expanduser().resolve()
        return path

    def ensure_directories_exist(self) -> None:
        """Create necessary directories if they don't exist."""
        self.get_storage_path().mkdir(parents=True, exist_ok=True)
        self.get_templates_path().mkdir(parents=True, exist_ok=True)


# Global config instance (lazy loaded)
_config: Optional[Config] = None


def get_config() -> Config:
    """Get global configuration instance."""
    global _config
    if _config is None:
        try:
            _config = Config()
        except ValueError as e:
            raise MissingEnvironmentVariableError(
                f"Configuration error: {e}\n"
                "Please check your environment variables. "
                "See .env.example for required variables."
            ) from e
    return _config


def reload_config() -> None:
    """Reload configuration (useful for testing)."""
    global _config
    _config = None
