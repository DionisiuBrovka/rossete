"""
Block type registry for Rossete.

Manages registration and instantiation of block generators.
"""

import logging
from typing import Dict, List, Optional, Type

from ..constants import BlockType
from ..exceptions import BlockRegistryError, BlockTypeNotFoundError
from .base import Block

logger = logging.getLogger(__name__)


class BlockRegistry:
    """Registry for block types and generators."""

    def __init__(self):
        """Initialize block registry."""
        self._registry: Dict[BlockType, Type[Block]] = {}
        logger.debug("Initialized BlockRegistry")

    def register(self, block_type: BlockType, block_class: Type[Block]) -> None:
        """
        Register a block type.

        Args:
            block_type: BlockType enum value
            block_class: Block class implementing the type

        Raises:
            BlockRegistryError: If type is already registered
        """
        if block_type in self._registry:
            raise BlockRegistryError(f"Block type {block_type.value} is already registered")

        # Validate that block_class is a Block subclass
        if not issubclass(block_class, Block):
            raise BlockRegistryError(
                f"Block class {block_class.__name__} must inherit from Block"
            )

        self._registry[block_type] = block_class
        logger.debug(f"Registered block type: {block_type.value}")

    def get(self, block_type: BlockType) -> Type[Block]:
        """
        Get block class by type.

        Args:
            block_type: BlockType enum value

        Returns:
            Block class

        Raises:
            BlockTypeNotFoundError: If type is not registered
        """
        if block_type not in self._registry:
            raise BlockTypeNotFoundError(
                f"Block type {block_type.value} is not registered. "
                f"Available types: {self.list_available()}"
            )

        return self._registry[block_type]

    def instantiate(self, block_type: BlockType) -> Block:
        """
        Create an instance of a block type.

        Args:
            block_type: BlockType enum value

        Returns:
            Block instance

        Raises:
            BlockTypeNotFoundError: If type is not registered
        """
        block_class = self.get(block_type)
        return block_class()

    def list_available(self) -> List[str]:
        """
        List all registered block types.

        Returns:
            List of block type names
        """
        return [block_type.value for block_type in self._registry.keys()]

    def is_registered(self, block_type: BlockType) -> bool:
        """
        Check if a block type is registered.

        Args:
            block_type: BlockType enum value

        Returns:
            True if registered, False otherwise
        """
        return block_type in self._registry

    def get_all(self) -> Dict[BlockType, Type[Block]]:
        """
        Get all registered blocks.

        Returns:
            Dictionary mapping BlockType to Block class
        """
        return self._registry.copy()

    def clear(self) -> None:
        """Clear all registrations (useful for testing)."""
        self._registry.clear()
        logger.debug("Cleared BlockRegistry")


# Global registry instance
_registry: Optional[BlockRegistry] = None


def get_block_registry() -> BlockRegistry:
    """
    Get global block registry instance.

    Returns:
        BlockRegistry instance
    """
    global _registry
    if _registry is None:
        _registry = BlockRegistry()
        _load_default_blocks()
    return _registry


def _load_default_blocks() -> None:
    """Load default block implementations into registry."""
    # Import here to avoid circular imports
    from .implementations import (
        AppendixBlock,
        IntroductionBlock,
        KeyTakeawaysBlock,
        LearningOutcomesBlock,
        MainContentBlock,
        PracticalTaskBlock,
        QuestionsBlock,
        ReferencesBlock,
        TitlePageBlock,
    )

    registry = _registry
    if registry is None:
        return

    blocks = [
        (BlockType.TITLE_PAGE, TitlePageBlock),
        (BlockType.INTRODUCTION, IntroductionBlock),
        (BlockType.MAIN_CONTENT, MainContentBlock),
        (BlockType.KEY_TAKEAWAYS, KeyTakeawaysBlock),
        (BlockType.REFERENCES, ReferencesBlock),
        (BlockType.PRACTICAL_TASK, PracticalTaskBlock),
        (BlockType.QUESTIONS, QuestionsBlock),
        (BlockType.LEARNING_OUTCOMES, LearningOutcomesBlock),
        (BlockType.APPENDIX, AppendixBlock),
    ]

    for block_type, block_class in blocks:
        try:
            registry.register(block_type, block_class)
        except BlockRegistryError as e:
            logger.warning(f"Could not register {block_type.value}: {e}")


def reset_block_registry() -> None:
    """Reset registry (useful for testing)."""
    global _registry
    _registry = None
