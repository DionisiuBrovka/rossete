"""
Practical task block implementation.
"""

from ..base import Block, BlockContent, BlockContext
from ...constants import BlockType
from ...exceptions import BlockGenerationError


class PracticalTaskBlock(Block):
    """Generates practical exercises and tasks."""

    @property
    def block_type(self) -> BlockType:
        """Return block type."""
        return BlockType.PRACTICAL_TASK

    async def generate(self, context: BlockContext) -> BlockContent:
        """Generate practical tasks."""
        if not context.ai_client:
            raise BlockGenerationError("AI client is required for tasks generation")

        system_prompt = self.get_system_prompt(context)
        user_prompt = self.get_user_prompt(context)

        content = await context.ai_client.generate_content(
            prompt=user_prompt,
            system_msg=system_prompt,
            max_tokens=1500,
            temperature=0.7,
        )

        return BlockContent(
            text=content,
            metadata={"block_type": self.block_type.value},
            formatting={"heading_level": 2},
        )

    def get_user_prompt(self, context: BlockContext) -> str:
        """Get user prompt for practical tasks."""
        task_count = context.parameters.get("task_count", 5)
        complexity = context.parameters.get("complexity", context.level)

        prompt = f"""Create {task_count} practical tasks for a {context.level} course on "{context.topic}".

Language: {context.language}
Complexity: {complexity}

For each task provide:
1. Task title
2. Objective (what learner will accomplish)
3. Detailed instructions
4. Expected outcomes
5. Success criteria
6. Hints (if needed)
7. Additional resources

Task characteristics:
- Progressive difficulty
- Real-world applications
- Hands-on implementation
- Clear deliverables
- Estimated time to complete

Make sure tasks:
- Build on course content
- Develop practical skills
- Are achievable within expected timeframe
- Have clear success criteria"""

        return prompt
