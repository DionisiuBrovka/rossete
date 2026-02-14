"""
Base classes for document blocks.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from ..ai.groq_client import GroqClient
from ..constants import BlockType


@dataclass
class BlockContext:
    """Context information for block generation."""

    topic: str
    level: str  # beginner, intermediate, advanced
    parameters: Dict[str, Any] = field(default_factory=dict)
    language: str = "en"
    ai_client: Optional[GroqClient] = None
    block_index: int = 0
    total_blocks: int = 0
    previous_block_content: Optional[str] = None


@dataclass
class BlockContent:
    """Generated block content."""

    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    formatting: Dict[str, Any] = field(default_factory=dict)
    block_type: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "text": self.text,
            "metadata": self.metadata,
            "formatting": self.formatting,
            "block_type": self.block_type,
        }


class Block(ABC):
    """Abstract base class for document blocks."""

    @property
    @abstractmethod
    def block_type(self) -> BlockType:
        """Return block type identifier."""
        pass

    @abstractmethod
    async def generate(self, context: BlockContext) -> BlockContent:
        """
        Generate block content.

        Args:
            context: BlockContext with generation parameters

        Returns:
            BlockContent with generated text and metadata

        Raises:
            GroqAPIError: If API call fails
            BlockGenerationError: If generation fails
        """
        pass

    def validate(self, content: BlockContent) -> bool:
        """
        Validate generated block content.

        Args:
            content: BlockContent to validate

        Returns:
            True if content is valid
        """
        # Default validation: non-empty content
        return bool(content.text and content.text.strip())

    def get_system_prompt(self, context: BlockContext) -> str:
        """
        Get system prompt for block generation.

        Args:
            context: BlockContext with generation parameters

        Returns:
            System prompt string
        """
        return (
            f"You are an expert educator creating {context.language} educational content. "
            f"Your role is to generate high-quality {self.block_type.value} for {context.level} learners. "
            f"Maintain clarity, accuracy, and engagement. "
            f"Focus on pedagogical soundness while being accessible to your target audience."
        )

    def get_user_prompt(self, context: BlockContext) -> str:
        """
        Get user prompt for block generation.

        Args:
            context: BlockContext with generation parameters

        Returns:
            User prompt string
        """
        raise NotImplementedError(
            f"Subclass {self.__class__.__name__} must implement get_user_prompt()"
        )
