"""
References block implementation.
"""

from ..base import Block, BlockContent, BlockContext
from ...constants import BlockType
from ...exceptions import BlockGenerationError


class ReferencesBlock(Block):
    """Generates bibliography and references."""

    @property
    def block_type(self) -> BlockType:
        """Return block type."""
        return BlockType.REFERENCES

    async def generate(self, context: BlockContext) -> BlockContent:
        """Generate references."""
        if not context.ai_client:
            raise BlockGenerationError("AI client is required for references generation")

        system_prompt = self.get_system_prompt(context)
        user_prompt = self.get_user_prompt(context)

        content = await context.ai_client.generate_content(
            prompt=user_prompt,
            system_msg=system_prompt,
            max_tokens=800,
            temperature=0.5,
        )

        return BlockContent(
            text=content,
            metadata={"block_type": self.block_type.value},
            formatting={"heading_level": 2},
        )

    def get_user_prompt(self, context: BlockContext) -> str:
        """Get user prompt for references."""
        prompt = f"""Create a bibliography for a {context.level} course on "{context.topic}".

Language: {context.language}
Citation format: APA style

Provide:
1. 15-20 key academic references (books, journals, papers)
2. Websites and online resources
3. Video tutorials or online courses (if relevant)
4. Supplementary materials

For each reference, include:
- Full citation in APA format
- Brief description of relevance (1-2 sentences)
- Suggested use in the curriculum

The references should cover:
- Foundational texts
- Recent research
- Practical applications
- Different perspectives on the topic"""

        return prompt
