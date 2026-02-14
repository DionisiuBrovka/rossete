"""
Appendix block implementation.
"""

from ..base import Block, BlockContent, BlockContext
from ...constants import BlockType
from ...exceptions import BlockGenerationError


class AppendixBlock(Block):
    """Generates appendix with supplementary materials."""

    @property
    def block_type(self) -> BlockType:
        """Return block type."""
        return BlockType.APPENDIX

    async def generate(self, context: BlockContext) -> BlockContent:
        """Generate appendix content."""
        if not context.ai_client:
            raise BlockGenerationError("AI client is required for appendix generation")

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
        """Get user prompt for appendix."""
        include_code = context.parameters.get("include_code_snippets", False)
        include_tables = context.parameters.get("include_tables", False)

        sections = ["Glossary of terms", "Quick reference guides"]

        if include_code:
            sections.append("Code samples and templates")

        if include_tables:
            sections.append("Reference tables and charts")

        sections_str = "\n".join([f"- {s}" for s in sections])

        prompt = f"""Create comprehensive appendix materials for a {context.level} course on "{context.topic}".

Language: {context.language}

Include the following sections:
{sections_str}
- Additional resources and tools
- Troubleshooting common issues

For each section provide:
1. Clear title
2. Organized content
3. Easy-to-scan format (tables, lists where appropriate)
4. Practical utility

Content requirements:
- Alphabetically organized where applicable
- Cross-references to main document sections
- Quick lookup capability
- Examples where helpful

The appendix should:
- Support learning and retention
- Provide quick reference
- Supplement main course material
- Be easy to navigate"""

        return prompt
