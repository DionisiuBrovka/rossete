"""
Key takeaways block implementation.
"""

from ..base import Block, BlockContent, BlockContext
from ...constants import BlockType
from ...exceptions import BlockGenerationError


class KeyTakeawaysBlock(Block):
    """Generates key takeaways and summary section."""

    @property
    def block_type(self) -> BlockType:
        """Return block type."""
        return BlockType.KEY_TAKEAWAYS

    async def generate(self, context: BlockContext) -> BlockContent:
        """Generate key takeaways."""
        if not context.ai_client:
            raise BlockGenerationError("AI client is required for takeaways generation")

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
        """Get user prompt for key takeaways."""
        prompt = f"""Create key takeaways and summary for a {context.level} course on "{context.topic}".

Language: {context.language}

Provide:
1. 5-7 most important concepts (as bullet points)
2. Critical principles to remember
3. Common misconceptions to avoid
4. Practical applications in real-world contexts

Format: Mix of bullet points and short paragraphs.
Length: Approximately 700-800 words.
Style: Concise, memorable, action-oriented.

Ensure takeaways are:
- Directly aligned with learning objectives
- Memorable and easy to recall
- Practically applicable"""

        return prompt
