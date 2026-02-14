"""
File storage for Rossete.

Manages persistent storage of generated documents.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..exceptions import DirectoryError, DocumentNotFoundError, StorageError

logger = logging.getLogger(__name__)


class FileStorage:
    """Manages document storage."""

    def __init__(self, base_path: Path):
        """
        Initialize file storage.

        Args:
            base_path: Base path for storage
        """
        self.base_path = Path(base_path).expanduser().resolve()
        logger.debug(f"Initialized FileStorage with base path: {base_path}")

    def ensure_directories(self) -> None:
        """Create necessary directories."""
        try:
            self.base_path.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Ensured storage directory exists: {self.base_path}")
        except OSError as e:
            logger.error(f"Failed to create storage directory: {e}")
            raise DirectoryError(f"Failed to create storage directory: {e}") from e

    def save_document(
        self, document_id: str, content: bytes, filename: str, metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Save document to storage.

        Args:
            document_id: Document identifier
            content: Document content
            filename: Filename to save as
            metadata: Optional metadata dictionary

        Returns:
            Path to saved file

        Raises:
            StorageError: If save fails
        """
        try:
            self.ensure_directories()

            # Create date-based subdirectory
            date_dir = self.base_path / datetime.now().strftime("%Y-%m-%d")
            date_dir.mkdir(parents=True, exist_ok=True)

            # Create document directory
            doc_dir = date_dir / f"doc_{document_id}"
            doc_dir.mkdir(parents=True, exist_ok=True)

            # Save file
            file_path = doc_dir / filename
            file_path.write_bytes(content)

            logger.info(f"Saved document to: {file_path}")

            # Save metadata if provided
            if metadata:
                self._save_metadata(doc_dir, document_id, metadata)

            return str(file_path)

        except OSError as e:
            logger.error(f"Failed to save document {document_id}: {e}")
            raise StorageError(f"Failed to save document: {e}") from e

    def save_text(
        self, document_id: str, content: str, filename: str, metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Save text document.

        Args:
            document_id: Document identifier
            content: Text content
            filename: Filename
            metadata: Optional metadata

        Returns:
            Path to saved file
        """
        return self.save_document(document_id, content.encode("utf-8"), filename, metadata)

    def get_document_path(self, document_id: str) -> Optional[Path]:
        """
        Get path to stored document.

        Args:
            document_id: Document identifier

        Returns:
            Path if found, None otherwise
        """
        # Search for document in date directories
        for date_dir in sorted(self.base_path.glob("*"), reverse=True):
            if not date_dir.is_dir():
                continue

            doc_dir = date_dir / f"doc_{document_id}"
            if doc_dir.exists():
                return doc_dir

        return None

    def list_documents(self) -> List[Dict[str, Any]]:
        """
        List all stored documents.

        Returns:
            List of document metadata
        """
        documents = []

        for date_dir in sorted(self.base_path.glob("*"), reverse=True):
            if not date_dir.is_dir():
                continue

            for doc_dir in date_dir.glob("doc_*"):
                if not doc_dir.is_dir():
                    continue

                # Get metadata if available
                metadata_path = doc_dir / "metadata.json"
                if metadata_path.exists():
                    try:
                        with open(metadata_path, "r", encoding="utf-8") as f:
                            metadata = json.load(f)
                        documents.append(metadata)
                    except (IOError, json.JSONDecodeError):
                        pass

        return documents

    def delete_document(self, document_id: str) -> bool:
        """
        Delete stored document.

        Args:
            document_id: Document identifier

        Returns:
            True if deleted, False if not found
        """
        doc_path = self.get_document_path(document_id)

        if not doc_path:
            return False

        try:
            import shutil

            shutil.rmtree(doc_path)
            logger.info(f"Deleted document: {document_id}")
            return True

        except OSError as e:
            logger.error(f"Failed to delete document {document_id}: {e}")
            return False

    def _save_metadata(self, doc_dir: Path, document_id: str, metadata: Dict[str, Any]) -> None:
        """Save metadata file."""
        try:
            metadata_path = doc_dir / "metadata.json"
            metadata_with_timestamp = {**metadata, "saved_at": datetime.now().isoformat()}

            with open(metadata_path, "w", encoding="utf-8") as f:
                json.dump(metadata_with_timestamp, f, indent=2, ensure_ascii=False)

            logger.debug(f"Saved metadata for document {document_id}")

        except (IOError, json.JSONDecodeError) as e:
            logger.warning(f"Failed to save metadata: {e}")
