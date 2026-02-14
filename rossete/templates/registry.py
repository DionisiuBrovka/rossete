"""
Template registry for Rossete.

Manages loading and retrieval of template definitions.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..constants import BlockType
from ..exceptions import TemplateError, TemplateNotFoundError, TemplateValidationError

logger = logging.getLogger(__name__)


class TemplateRegistry:
    """Registry for managing templates."""

    def __init__(self, templates_path: Path):
        """
        Initialize template registry.

        Args:
            templates_path: Path to templates directory
        """
        self.templates_path = Path(templates_path)
        self._templates: Dict[str, Dict[str, Any]] = {}
        self._loaded = False
        logger.debug(f"Initialized TemplateRegistry with path: {templates_path}")

    def load_templates(self) -> None:
        """Load all templates from disk."""
        if self._loaded:
            return

        if not self.templates_path.exists():
            logger.warning(f"Templates path does not exist: {self.templates_path}")
            self._loaded = True
            return

        # Look for JSON template files
        template_files = list(self.templates_path.glob("**/*.json"))
        logger.info(f"Found {len(template_files)} template files")

        for template_file in template_files:
            try:
                self._load_template_file(template_file)
            except TemplateError as e:
                logger.warning(f"Failed to load template {template_file}: {e}")

        self._loaded = True
        logger.info(f"Loaded {len(self._templates)} templates")

    def _load_template_file(self, file_path: Path) -> None:
        """
        Load single template file.

        Args:
            file_path: Path to template JSON file

        Raises:
            TemplateError: If template is invalid
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                template_data = json.load(f)

            # Validate template structure
            self._validate_template(template_data)

            template_id = template_data.get("id")
            if not template_id:
                raise TemplateValidationError("Template missing 'id' field")

            self._templates[template_id] = template_data
            logger.debug(f"Loaded template: {template_id}")

        except json.JSONDecodeError as e:
            raise TemplateError(f"Invalid JSON in template file {file_path}: {e}") from e
        except IOError as e:
            raise TemplateError(f"Failed to read template file {file_path}: {e}") from e

    def _validate_template(self, template: Dict[str, Any]) -> None:
        """
        Validate template structure.

        Args:
            template: Template dictionary

        Raises:
            TemplateValidationError: If template is invalid
        """
        required_fields = ["id", "name", "blocks"]
        for field in required_fields:
            if field not in template:
                raise TemplateValidationError(f"Template missing required field: {field}")

        if not isinstance(template["blocks"], list):
            raise TemplateValidationError("Template 'blocks' must be a list")

        if len(template["blocks"]) == 0:
            raise TemplateValidationError("Template must have at least one block")

        # Validate blocks
        for block in template["blocks"]:
            if "type" not in block:
                raise TemplateValidationError("Block missing 'type' field")

            # Check if block type is valid
            valid_types = [bt.value for bt in BlockType]
            if block["type"] not in valid_types:
                raise TemplateValidationError(
                    f"Invalid block type: {block['type']}. "
                    f"Valid types: {valid_types}"
                )

    def get(self, template_id: str) -> Dict[str, Any]:
        """
        Get template by ID.

        Args:
            template_id: Template identifier

        Returns:
            Template dictionary

        Raises:
            TemplateNotFoundError: If template not found
        """
        self.load_templates()

        if template_id not in self._templates:
            raise TemplateNotFoundError(
                f"Template '{template_id}' not found. "
                f"Available templates: {list(self._templates.keys())}"
            )

        return self._templates[template_id].copy()

    def list_templates(self) -> List[Dict[str, Any]]:
        """
        List all available templates.

        Returns:
            List of template metadata dictionaries
        """
        self.load_templates()

        templates = []
        for template_id, template_data in self._templates.items():
            templates.append(
                {
                    "id": template_id,
                    "name": template_data.get("name", "Unknown"),
                    "description": template_data.get("description", ""),
                    "document_type": template_data.get("document_type", "unknown"),
                    "version": template_data.get("version", "1.0"),
                    "block_count": len(template_data.get("blocks", [])),
                }
            )

        return templates

    def template_exists(self, template_id: str) -> bool:
        """
        Check if template exists.

        Args:
            template_id: Template identifier

        Returns:
            True if template exists, False otherwise
        """
        self.load_templates()
        return template_id in self._templates

    def clear_cache(self) -> None:
        """Clear template cache (useful for testing)."""
        self._templates.clear()
        self._loaded = False
        logger.debug("Cleared template cache")


# Global registry instance
_registry: Optional[TemplateRegistry] = None


def get_template_registry(templates_path: Optional[Path] = None) -> TemplateRegistry:
    """
    Get or create template registry.

    Args:
        templates_path: Path to templates directory (optional)

    Returns:
        TemplateRegistry instance
    """
    global _registry

    if _registry is None:
        if templates_path is None:
            from ..config import get_config

            config = get_config()
            templates_path = config.get_templates_path()

        _registry = TemplateRegistry(templates_path)

    return _registry


def reset_template_registry() -> None:
    """Reset template registry (useful for testing)."""
    global _registry
    _registry = None
