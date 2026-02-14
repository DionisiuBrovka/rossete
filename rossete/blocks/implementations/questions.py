"""
Questions block implementation.
"""

from ..base import Block, BlockContent, BlockContext
from ...constants import BlockType
from ...exceptions import BlockGenerationError


class QuestionsBlock(Block):
    """Generates quiz and review questions."""

    @property
    def block_type(self) -> BlockType:
        """Return block type."""
        return BlockType.QUESTIONS

    async def generate(self, context: BlockContext) -> BlockContent:
        """Generate review questions."""
        if not context.ai_client:
            raise BlockGenerationError("AI client is required for questions generation")

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
        """Get user prompt for questions."""
        question_count = context.parameters.get("question_count", 10)
        difficulty = context.parameters.get("difficulty", context.level)

        prompt = f"""Create {question_count} review and assessment questions for a {context.level} course on "{context.topic}".

Language: {context.language}
Difficulty: {difficulty}

Include mix of:
1. Multiple choice questions (5 options, 1 correct)
2. Short answer questions
3. Essay/discussion questions
4. Application-based scenarios

For each question provide:
- Question text
- Question type
- For multiple choice: all 5 options
- For essay: expected answer outline
- Difficulty level
- Learning objective covered

Questions should:
- Test comprehension and application
- Cover all major topics
- Be clear and unambiguous
- Have definitive correct answers
- Progress from basic to advanced (if applicable)"""

        return prompt
