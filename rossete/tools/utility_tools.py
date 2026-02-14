"""
Utility tools for MCP.
"""

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def list_block_types() -> Dict[str, Any]:
    """
    List all available block types.

    Returns:
        Dictionary with block type information
    """
    try:
        from ..constants import BlockType, BLOCK_TYPE_TOKEN_LIMITS
        from ..blocks import get_block_registry

        registry = get_block_registry()
        available_types = registry.list_available()

        block_info = []
        for block_type_str in available_types:
            block_type = BlockType(block_type_str)
            block_info.append(
                {
                    "type": block_type_str,
                    "max_tokens": BLOCK_TYPE_TOKEN_LIMITS.get(block_type, 2000),
                }
            )

        return {
            "success": True,
            "count": len(block_info),
            "block_types": block_info,
        }

    except Exception as e:
        logger.error(f"Failed to list block types: {e}")
        return {
            "success": False,
            "error": str(e),
            "block_types": [],
        }


def get_block_type_details(block_type: str) -> Dict[str, Any]:
    """
    Get details about a specific block type.

    Args:
        block_type: Block type identifier

    Returns:
        Dictionary with block details
    """
    try:
        from ..constants import BlockType, BLOCK_TYPE_TOKEN_LIMITS
        from ..blocks import get_block_registry

        # Validate block type
        try:
            bt = BlockType(block_type)
        except ValueError:
            return {
                "success": False,
                "error": f"Unknown block type: {block_type}",
            }

        registry = get_block_registry()

        if not registry.is_registered(bt):
            return {
                "success": False,
                "error": f"Block type not registered: {block_type}",
            }

        return {
            "success": True,
            "block_type": block_type,
            "max_tokens": BLOCK_TYPE_TOKEN_LIMITS.get(bt, 2000),
            "registered": True,
        }

    except Exception as e:
        logger.error(f"Failed to get block type details: {e}")
        return {
            "success": False,
            "error": str(e),
        }


def validate_parameters(template_id: str, parameters: str = "{}") -> Dict[str, Any]:
    """
    Validate parameters for a template.

    Args:
        template_id: Template identifier
        parameters: JSON string with parameters

    Returns:
        Dictionary with validation result
    """
    try:
        import json

        # Parse parameters
        try:
            params = json.loads(parameters) if isinstance(parameters, str) else parameters
        except json.JSONDecodeError:
            return {
                "success": False,
                "error": "Invalid parameters JSON",
                "valid": False,
            }

        # Check if template exists
        from ..config import get_config
        from ..templates import get_template_registry

        config = get_config()
        registry = get_template_registry(config.get_templates_path())

        if not registry.template_exists(template_id):
            return {
                "success": False,
                "error": f"Template not found: {template_id}",
                "valid": False,
            }

        # Basic validation
        if not isinstance(params, dict):
            return {
                "success": False,
                "error": "Parameters must be a dictionary",
                "valid": False,
            }

        return {
            "success": True,
            "valid": True,
            "message": "Parameters are valid",
        }

    except Exception as e:
        logger.error(f"Parameter validation error: {e}")
        return {
            "success": False,
            "error": str(e),
            "valid": False,
        }


def get_server_info() -> Dict[str, Any]:
    """
    Get server information and status.

    Returns:
        Dictionary with server info
    """
    try:
        from .. import __version__
        from ..config import get_config

        config = get_config()

        return {
            "success": True,
            "version": __version__,
            "groq_model": config.groq_model,
            "storage_path": str(config.get_storage_path()),
            "templates_path": str(config.get_templates_path()),
            "max_concurrent": config.max_concurrent_requests,
            "max_blocks": config.max_blocks_per_document,
        }

    except Exception as e:
        logger.error(f"Failed to get server info: {e}")
        return {
            "success": False,
            "error": str(e),
        }
