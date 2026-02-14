"""
Base class for exporters.
"""

from abc import ABC, abstractmethod
from typing import List

from ..blocks import BlockContent


class Exporter(ABC):
    """Abstract base class for document exporters."""

    @property
    @abstractmethod
    def format_name(self) -> str:
        """Return export format name (e.g., 'docx', 'pdf', 'markdown')."""
        pass

    @abstractmethod
    def export(self, blocks: List[BlockContent], output_path: str) -> bool:
        """
        Export blocks to file.

        Args:
            blocks: List of BlockContent objects
            output_path: Path for output file

        Returns:
            True if export successful

        Raises:
            ExportError: If export fails
        """
        pass

    def validate_blocks(self, blocks: List[BlockContent]) -> bool:
        """
        Validate blocks before export.

        Args:
            blocks: List of BlockContent objects

        Returns:
            True if valid
        """
        if not blocks:
            return False

        for block in blocks:
            if not block.text or not block.text.strip():
                return False

        return True
