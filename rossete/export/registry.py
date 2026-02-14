"""
Exporter registry for Rossete.
"""

import logging
from typing import Dict, List, Optional, Type

from ..exceptions import ExporterNotFoundError, UnsupportedFormatError
from .base import Exporter

logger = logging.getLogger(__name__)


class ExporterRegistry:
    """Registry for document exporters."""

    def __init__(self):
        """Initialize exporter registry."""
        self._exporters: Dict[str, Type[Exporter]] = {}
        logger.debug("Initialized ExporterRegistry")

    def register(self, format_name: str, exporter_class: Type[Exporter]) -> None:
        """
        Register an exporter.

        Args:
            format_name: Format identifier (e.g., 'docx', 'pdf', 'markdown')
            exporter_class: Exporter class
        """
        if not issubclass(exporter_class, Exporter):
            raise ValueError(f"{exporter_class} must inherit from Exporter")

        self._exporters[format_name.lower()] = exporter_class
        logger.debug(f"Registered exporter: {format_name}")

    def get(self, format_name: str) -> Type[Exporter]:
        """
        Get exporter by format.

        Args:
            format_name: Format identifier

        Returns:
            Exporter class

        Raises:
            UnsupportedFormatError: If format not supported
        """
        format_key = format_name.lower()

        if format_key not in self._exporters:
            available = list(self._exporters.keys())
            raise UnsupportedFormatError(
                f"Format '{format_name}' not supported. "
                f"Available formats: {available}"
            )

        return self._exporters[format_key]

    def instantiate(self, format_name: str) -> Exporter:
        """
        Create exporter instance.

        Args:
            format_name: Format identifier

        Returns:
            Exporter instance
        """
        exporter_class = self.get(format_name)
        return exporter_class()

    def list_formats(self) -> List[str]:
        """List all supported formats."""
        return sorted(self._exporters.keys())

    def is_supported(self, format_name: str) -> bool:
        """Check if format is supported."""
        return format_name.lower() in self._exporters


# Global registry
_registry: Optional[ExporterRegistry] = None


def get_exporter_registry() -> ExporterRegistry:
    """Get or create exporter registry."""
    global _registry

    if _registry is None:
        _registry = ExporterRegistry()
        _load_default_exporters()

    return _registry


def _load_default_exporters() -> None:
    """Load default exporters."""
    from .docx_exporter import DocxExporter
    from .markdown_exporter import MarkdownExporter

    registry = _registry
    if registry is None:
        return

    registry.register("docx", DocxExporter)
    registry.register("markdown", MarkdownExporter)

    logger.debug("Loaded default exporters")


def reset_exporter_registry() -> None:
    """Reset registry (for testing)."""
    global _registry
    _registry = None
