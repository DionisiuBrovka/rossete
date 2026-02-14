"""
Template management tools for MCP.
"""

import json
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def list_templates() -> Dict[str, Any]:
    """
    List all available templates.

    Returns:
        Dictionary with list of templates
    """
    try:
        from ..config import get_config
        from ..templates import get_template_registry

        config = get_config()
        registry = get_template_registry(config.get_templates_path())

        templates = registry.list_templates()

        return {
            "success": True,
            "count": len(templates),
            "templates": templates,
        }

    except Exception as e:
        logger.error(f"Failed to list templates: {e}")
        return {
            "success": False,
            "error": str(e),
            "templates": [],
        }


def get_template_details(template_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a template.

    Args:
        template_id: Template identifier

    Returns:
        Dictionary with template details
    """
    try:
        from ..config import get_config
        from ..templates import get_template_registry

        config = get_config()
        registry = get_template_registry(config.get_templates_path())

        template = registry.get(template_id)

        return {
            "success": True,
            "template": template,
        }

    except Exception as e:
        logger.error(f"Failed to get template details: {e}")
        return {
            "success": False,
            "error": str(e),
        }


def create_custom_template(
    name: str,
    document_type: str,
    blocks: str,
) -> Dict[str, Any]:
    """
    Create a custom template.

    Args:
        name: Template name
        document_type: Document type
        blocks: JSON string with block configuration

    Returns:
        Dictionary with creation status
    """
    try:
        # Parse blocks JSON
        try:
            blocks_list = json.loads(blocks) if isinstance(blocks, str) else blocks
        except json.JSONDecodeError:
            return {
                "success": False,
                "error": "Invalid blocks JSON",
            }

        # For now, just validate
        if not isinstance(blocks_list, list):
            return {
                "success": False,
                "error": "Blocks must be a list",
            }

        if len(blocks_list) == 0:
            return {
                "success": False,
                "error": "At least one block is required",
            }

        return {
            "success": True,
            "message": "Custom template validation passed",
            "block_count": len(blocks_list),
        }

    except Exception as e:
        logger.error(f"Failed to create custom template: {e}")
        return {
            "success": False,
            "error": str(e),
        }
