"""
Document generation tools for MCP.
"""

import json
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


async def generate_document(
    template_id: str,
    topic: str,
    level: str = "intermediate",
    parameters: str = "{}",
) -> Dict[str, Any]:
    """
    Generate an educational document from a template.

    Args:
        template_id: Template identifier (e.g., 'lecture_standard_v1')
        topic: Document topic
        level: Difficulty level (beginner, intermediate, advanced)
        parameters: JSON string with additional parameters

    Returns:
        Dictionary with document info and generation status
    """
    try:
        from ..config import get_config
        from ..generator import DocumentGenerator

        # Parse parameters
        try:
            params = json.loads(parameters) if isinstance(parameters, str) else parameters
        except json.JSONDecodeError:
            return {
                "success": False,
                "error": "Invalid parameters JSON",
                "document_id": None,
            }

        # Create generator and generate
        config = get_config()
        generator = DocumentGenerator(config)

        result = await generator.generate_document(
            template_id=template_id,
            topic=topic,
            level=level,
            parameters=params,
        )

        return {
            "success": result.success,
            "document_id": result.document_id,
            "output_file": result.output_file,
            "generation_time_seconds": result.generation_time_seconds,
            "tokens_used": result.tokens_used,
            "error": result.error,
            "metadata": result.metadata,
        }

    except Exception as e:
        logger.error(f"Document generation error: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e),
            "document_id": None,
        }


def export_document(document_id: str, format: str = "docx") -> Dict[str, Any]:
    """
    Export a previously generated document to different format.

    Args:
        document_id: Document identifier
        format: Export format (docx, pdf, markdown)

    Returns:
        Dictionary with export status
    """
    try:
        from ..config import get_config
        from ..storage import FileStorage

        config = get_config()
        storage = FileStorage(config.get_storage_path())

        doc_path = storage.get_document_path(document_id)

        if not doc_path:
            return {
                "success": False,
                "error": f"Document '{document_id}' not found",
            }

        return {
            "success": True,
            "document_path": str(doc_path),
            "formats_available": ["md"],  # Other formats based on what's saved
        }

    except Exception as e:
        logger.error(f"Export error: {e}")
        return {
            "success": False,
            "error": str(e),
        }


def get_document_status(document_id: str) -> Dict[str, Any]:
    """
    Get status and metadata of a document.

    Args:
        document_id: Document identifier

    Returns:
        Dictionary with document status and metadata
    """
    try:
        from ..config import get_config
        from ..storage import FileStorage

        config = get_config()
        storage = FileStorage(config.get_storage_path())

        doc_path = storage.get_document_path(document_id)

        if not doc_path:
            return {
                "found": False,
                "document_id": document_id,
            }

        # Try to load metadata
        metadata_file = doc_path / "metadata.json"
        metadata = {}

        if metadata_file.exists():
            import json

            try:
                with open(metadata_file, "r") as f:
                    metadata = json.load(f)
            except Exception:
                pass

        return {
            "found": True,
            "document_id": document_id,
            "path": str(doc_path),
            "metadata": metadata,
        }

    except Exception as e:
        logger.error(f"Status check error: {e}")
        return {
            "found": False,
            "error": str(e),
        }
