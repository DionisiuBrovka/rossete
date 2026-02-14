"""
Main document generator for Rossete.

Orchestrates the document generation pipeline.
"""

import logging
import time
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional

from ..ai.groq_client import GroqClient, get_groq_client
from ..blocks import BlockContext, get_block_registry
from ..config import get_config
from ..constants import BlockType
from ..exceptions import (
    GenerationError,
    InvalidParametersError,
    TemplateNotFoundError,
)
from ..templates import get_template_registry

logger = logging.getLogger(__name__)


@dataclass
class GenerationResult:
    """Result of document generation."""

    success: bool
    document_id: str
    output_file: str
    format: str = "docx"
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    generation_time_seconds: float = 0.0
    tokens_used: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


class DocumentGenerator:
    """Main orchestrator for document generation."""

    def __init__(self, config: Optional[Any] = None):
        """
        Initialize document generator.

        Args:
            config: Configuration object (uses global if not provided)
        """
        self.config = config or get_config()
        self.template_registry = get_template_registry(self.config.get_templates_path())
        self.block_registry = get_block_registry()
        self.ai_client: Optional[GroqClient] = None
        logger.info("Initialized DocumentGenerator")

    def _initialize_ai_client(self) -> GroqClient:
        """Initialize or retrieve Groq client."""
        if self.ai_client is None:
            self.ai_client = get_groq_client(self.config.groq_api_key, self.config.groq_model)
        return self.ai_client

    async def generate_document(
        self,
        template_id: str,
        topic: str,
        level: str = "intermediate",
        parameters: Optional[Dict[str, Any]] = None,
    ) -> GenerationResult:
        """
        Generate document from template.

        Args:
            template_id: Template identifier
            topic: Document topic
            level: Difficulty level
            parameters: Optional additional parameters

        Returns:
            GenerationResult with document path and metadata
        """
        start_time = time.time()
        document_id = str(uuid.uuid4())[:8]
        parameters = parameters or {}

        try:
            logger.info(
                f"Starting document generation: {document_id}, "
                f"template={template_id}, topic={topic}"
            )

            # Load and validate template
            template = self.template_registry.get(template_id)
            logger.debug(f"Loaded template: {template_id}")

            # Validate parameters
            self._validate_parameters(template, parameters)

            # Initialize AI client
            ai_client = self._initialize_ai_client()

            # Generate blocks
            blocks = await self._generate_blocks(template, topic, level, parameters, ai_client)
            logger.info(f"Generated {len(blocks)} blocks for document {document_id}")

            # Get token usage
            usage_stats = ai_client.get_usage_stats()
            tokens_used = usage_stats.get("total_tokens", 0)

            # Generate metadata
            metadata = {
                "template_id": template_id,
                "topic": topic,
                "level": level,
                "block_count": len(blocks),
                "parameters": parameters,
            }

            generation_time = time.time() - start_time
            logger.info(
                f"Document generation completed: {document_id} "
                f"in {generation_time:.2f}s, tokens: {tokens_used}"
            )

            return GenerationResult(
                success=True,
                document_id=document_id,
                output_file=f"document_{document_id}.md",  # Placeholder
                metadata=metadata,
                generation_time_seconds=generation_time,
                tokens_used=tokens_used,
            )

        except (TemplateNotFoundError, InvalidParametersError, GenerationError) as e:
            logger.error(f"Generation failed for document {document_id}: {e}")
            generation_time = time.time() - start_time
            return GenerationResult(
                success=False,
                document_id=document_id,
                output_file="",
                error=str(e),
                generation_time_seconds=generation_time,
            )

        except Exception as e:
            logger.error(f"Unexpected error during generation {document_id}: {e}", exc_info=True)
            generation_time = time.time() - start_time
            return GenerationResult(
                success=False,
                document_id=document_id,
                output_file="",
                error=f"Unexpected error: {str(e)}",
                generation_time_seconds=generation_time,
            )

    async def _generate_blocks(
        self,
        template: Dict[str, Any],
        topic: str,
        level: str,
        parameters: Dict[str, Any],
        ai_client: GroqClient,
    ) -> List[str]:
        """
        Generate all blocks for document.

        Args:
            template: Template definition
            topic: Document topic
            level: Difficulty level
            parameters: Additional parameters
            ai_client: AI client for generation

        Returns:
            List of generated block contents
        """
        blocks = []
        template_blocks = template.get("blocks", [])

        logger.debug(f"Generating {len(template_blocks)} blocks")

        for index, block_spec in enumerate(template_blocks):
            try:
                block_type_str = block_spec.get("type")
                block_type = BlockType(block_type_str)

                logger.debug(f"Generating block {index + 1}/{len(template_blocks)}: {block_type_str}")

                # Get block instance
                block = self.block_registry.instantiate(block_type)

                # Create context
                context = BlockContext(
                    topic=topic,
                    level=level,
                    parameters={**parameters, **block_spec.get("parameters", {})},
                    language=parameters.get("language", "en"),
                    ai_client=ai_client,
                    block_index=index,
                    total_blocks=len(template_blocks),
                    previous_block_content=blocks[-1] if blocks else None,
                )

                # Generate block
                block_content = await block.generate(context)
                blocks.append(block_content.text)

                logger.debug(f"Successfully generated block: {block_type_str}")

            except Exception as e:
                logger.warning(f"Failed to generate block {index}: {e}")
                if block_spec.get("required", False):
                    raise GenerationError(f"Failed to generate required block: {e}") from e
                # Skip optional blocks that fail
                continue

        return blocks

    def _validate_parameters(self, template: Dict[str, Any], parameters: Dict[str, Any]) -> None:
        """
        Validate parameters against template requirements.

        Args:
            template: Template definition
            parameters: User parameters

        Raises:
            InvalidParametersError: If parameters are invalid
        """
        # Basic validation
        if not isinstance(parameters, dict):
            raise InvalidParametersError("Parameters must be a dictionary")

        # Check for supported parameters based on template
        # This can be extended with more sophisticated validation
        logger.debug("Parameters validated successfully")


# Convenience function
def create_generator(config: Optional[Any] = None) -> DocumentGenerator:
    """
    Create document generator instance.

    Args:
        config: Configuration object (optional)

    Returns:
        DocumentGenerator instance
    """
    return DocumentGenerator(config)
