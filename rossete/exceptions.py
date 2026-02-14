"""
Custom exceptions for Rossete.
"""


class RossetException(Exception):
    """Base exception for all Rossete errors."""

    pass


# Configuration Errors
class ConfigurationError(RossetException):
    """Raised when configuration is invalid or incomplete."""

    pass


class MissingEnvironmentVariableError(ConfigurationError):
    """Raised when a required environment variable is missing."""

    pass


# Template Errors
class TemplateError(RossetException):
    """Raised when there's an issue with template loading or validation."""

    pass


class TemplateNotFoundError(TemplateError):
    """Raised when a requested template is not found."""

    pass


class TemplateValidationError(TemplateError):
    """Raised when a template structure is invalid."""

    pass


# Block Generation Errors
class GenerationError(RossetException):
    """Base exception for document generation errors."""

    pass


class BlockGenerationError(GenerationError):
    """Raised when a block fails to generate."""

    pass


class GroqAPIError(GenerationError):
    """Raised when Groq API call fails."""

    pass


class GroqRateLimitError(GroqAPIError):
    """Raised when rate limit is exceeded."""

    pass


class GroqAuthenticationError(GroqAPIError):
    """Raised when authentication with Groq API fails."""

    pass


class TimeoutError(GenerationError):
    """Raised when operation times out."""

    pass


class InvalidParametersError(GenerationError):
    """Raised when parameters don't match template requirements."""

    pass


# Export Errors
class ExportError(RossetException):
    """Raised when document export fails."""

    pass


class UnsupportedFormatError(ExportError):
    """Raised when requested export format is not supported."""

    pass


class ExporterNotFoundError(ExportError):
    """Raised when requested exporter is not available."""

    pass


# Storage Errors
class StorageError(RossetException):
    """Raised when file storage operation fails."""

    pass


class DocumentNotFoundError(StorageError):
    """Raised when a document cannot be found in storage."""

    pass


class DirectoryError(StorageError):
    """Raised when directory operations fail."""

    pass


# Block Registry Errors
class BlockRegistryError(RossetException):
    """Raised when block registration fails."""

    pass


class BlockTypeNotFoundError(BlockRegistryError):
    """Raised when requested block type is not registered."""

    pass
