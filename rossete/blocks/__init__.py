"""
Block system for Rossete.

Defines block types and generators for document composition.
"""

from .base import Block, BlockContent, BlockContext
from .registry import BlockRegistry, get_block_registry

__all__ = ["Block", "BlockContent", "BlockContext", "BlockRegistry", "get_block_registry"]
