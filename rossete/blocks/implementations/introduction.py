"""
Introduction block implementation.
"""

from ..base import Block, BlockContent, BlockContext
from ...constants import BlockType
from ...exceptions import BlockGenerationError


class IntroductionBlock(Block):
    """Generates introduction section for document."""

    @property
    def block_type(self) -> BlockType:
        """Return block type."""
        return BlockType.INTRODUCTION

    async def generate(self, context: BlockContext) -> BlockContent:
        """Generate introduction content."""
        if not context.ai_client:
            raise BlockGenerationError("AI client is required for introduction generation")

        system_prompt = self.get_system_prompt(context)
        user_prompt = self.get_user_prompt(context)

        content = await context.ai_client.generate_content(
            prompt=user_prompt,
            system_msg=system_prompt,
            max_tokens=1000,
            temperature=0.7,
        )

        return BlockContent(
            text=content,
            metadata={"block_type": self.block_type.value},
            formatting={"heading_level": 2},
        )

    def get_user_prompt(self, context: BlockContext) -> str:
        """Get user prompt for introduction."""
        prompt = f"""Create an engaging introduction for a {context.level} course on "{context.topic}".

Include:
1. Hook or opening statement to engage learners
2. Course objectives (3-5 key learning goals)
3. What students will learn and be able to do
4. Prerequisites or prior knowledge needed (if any)
5. How this topic fits into the broader curriculum

Language: {context.language}
Format: Use clear sections with subheadings.
Length: Approximately 800-1000 words."""

        return prompt
