"""
Learning outcomes block implementation.
"""

from ..base import Block, BlockContent, BlockContext
from ...constants import BlockType
from ...exceptions import BlockGenerationError


class LearningOutcomesBlock(Block):
    """Generates learning outcomes and competencies."""

    @property
    def block_type(self) -> BlockType:
        """Return block type."""
        return BlockType.LEARNING_OUTCOMES

    async def generate(self, context: BlockContext) -> BlockContent:
        """Generate learning outcomes."""
        if not context.ai_client:
            raise BlockGenerationError("AI client is required for outcomes generation")

        system_prompt = self.get_system_prompt(context)
        user_prompt = self.get_user_prompt(context)

        content = await context.ai_client.generate_content(
            prompt=user_prompt,
            system_msg=system_prompt,
            max_tokens=800,
            temperature=0.7,
        )

        return BlockContent(
            text=content,
            metadata={"block_type": self.block_type.value},
            formatting={"heading_level": 2},
        )

    def get_user_prompt(self, context: BlockContext) -> str:
        """Get user prompt for learning outcomes."""
        prompt = f"""Create clear learning outcomes and competencies for a {context.level} course on "{context.topic}".

Language: {context.language}

Structure outcomes using Bloom's taxonomy levels:
1. Remember (recall definitions, facts)
2. Understand (explain concepts)
3. Apply (use knowledge in new situations)
4. Analyze (examine relationships)
5. Evaluate (make judgments)
6. Create (assemble new knowledge)

For each level, provide:
- 2-3 specific, measurable outcomes
- Observable action (using verbs like: list, identify, compare, analyze, evaluate, design)
- Clear success criteria
- How it relates to the course topic

Each outcome should:
- Be specific and measurable
- Include action verb
- Be achievable within course scope
- Build progressively in complexity
- Be aligned with industry standards (if applicable)

Total: 12-18 outcomes covering all levels"""

        return prompt
