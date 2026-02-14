"""
Title page block implementation.
"""

from datetime import datetime

from ..base import Block, BlockContent, BlockContext
from ...constants import BlockType


class TitlePageBlock(Block):
    """Generates title page for document."""

    @property
    def block_type(self) -> BlockType:
        """Return block type."""
        return BlockType.TITLE_PAGE

    async def generate(self, context: BlockContext) -> BlockContent:
        """Generate title page content."""
        title = context.parameters.get("title", context.topic)
        author = context.parameters.get("author", "Educational Department")
        group = context.parameters.get("group", "")
        date_str = datetime.now().strftime("%Y-%m-%d")

        content = f"""# {title}

**Author:** {author}
**Group:** {group}
**Date:** {date_str}
**Level:** {context.level.capitalize()}

---

## Course Overview

This document provides comprehensive educational material for the following topic:

**{context.topic}**

This material is designed for {context.level} learners and aims to provide a structured approach to understanding the subject matter.
"""

        return BlockContent(
            text=content,
            metadata={"block_type": self.block_type.value, "title": title},
            formatting={"heading_level": 1},
        )

    def get_user_prompt(self, context: BlockContext) -> str:
        """Get user prompt."""
        return f"Create title page for: {context.topic}"
