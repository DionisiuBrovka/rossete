"""
Main content block implementation.
"""

from ..base import Block, BlockContent, BlockContext
from ...constants import BlockType
from ...exceptions import BlockGenerationError


class MainContentBlock(Block):
    """Generates main lecture/course content."""

    @property
    def block_type(self) -> BlockType:
        """Return block type."""
        return BlockType.MAIN_CONTENT

    async def generate(self, context: BlockContext) -> BlockContent:
        """Generate main content."""
        if not context.ai_client:
            raise BlockGenerationError("AI client is required for content generation")

        system_prompt = self.get_system_prompt(context)
        user_prompt = self.get_user_prompt(context)

        content = await context.ai_client.generate_content(
            prompt=user_prompt,
            system_msg=system_prompt,
            max_tokens=6000,
            temperature=0.7,
        )

        return BlockContent(
            text=content,
            metadata={"block_type": self.block_type.value},
            formatting={"heading_level": 2},
        )

    def get_user_prompt(self, context: BlockContext) -> str:
        """Get user prompt for main content."""
        include_code = context.parameters.get("include_code_snippets", False)
        duration = context.parameters.get("duration_minutes", 90)

        code_note = (
            "\nInclude relevant code snippets and examples where appropriate.\n"
            if include_code
            else "\n"
        )

        prompt = f"""Create comprehensive main content for a {context.level} course on "{context.topic}".

Duration: {duration} minutes
Language: {context.language}{code_note}
Structure the content with:
1. Main concepts and definitions (with clear explanations)
2. Core principles and theories
3. Practical examples and applications
4. Common challenges and how to overcome them
5. Advanced considerations (if level is advanced)

Format: Use clear hierarchical sections with subheadings.
Style: Professional, academic, yet accessible.
Length: Comprehensive coverage (5000-6000 words)
Detail level: {context.level.capitalize()}

Ensure the content is self-contained and builds logically from simpler to more complex concepts."""

        return prompt
