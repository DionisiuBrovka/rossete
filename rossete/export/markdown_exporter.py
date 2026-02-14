"""
Markdown exporter for Rossete.
"""

import logging
from pathlib import Path
from typing import List

from ..blocks import BlockContent
from ..exceptions import ExportError
from .base import Exporter

logger = logging.getLogger(__name__)


class MarkdownExporter(Exporter):
    """Exports document to Markdown format."""

    @property
    def format_name(self) -> str:
        """Return format name."""
        return "markdown"

    def export(self, blocks: List[BlockContent], output_path: str) -> bool:
        """
        Export blocks to Markdown file.

        Args:
            blocks: List of BlockContent objects
            output_path: Path for output file

        Returns:
            True if successful

        Raises:
            ExportError: If export fails
        """
        try:
            if not self.validate_blocks(blocks):
                raise ExportError("No valid blocks to export")

            logger.debug(f"Exporting {len(blocks)} blocks to Markdown: {output_path}")

            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, "w", encoding="utf-8") as f:
                for block in blocks:
                    # Write block text
                    f.write(block.text)
                    f.write("\n\n")

                    # Add metadata as comment
                    if block.metadata:
                        f.write("<!-- Metadata:\n")
                        for key, value in block.metadata.items():
                            f.write(f"  {key}: {value}\n")
                        f.write("-->\n\n")

            logger.info(f"Successfully exported to Markdown: {output_path}")
            return True

        except IOError as e:
            logger.error(f"Failed to write Markdown file: {e}")
            raise ExportError(f"Failed to write Markdown file: {e}") from e
        except Exception as e:
            logger.error(f"Markdown export error: {e}")
            raise ExportError(f"Markdown export failed: {e}") from e
