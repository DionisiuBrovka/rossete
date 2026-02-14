"""
Constants, enums, and default values for Rossete.
"""

from enum import Enum

# Block Types
class BlockType(str, Enum):
    """Available block types for documents."""
    TITLE_PAGE = "title_page"
    INTRODUCTION = "introduction"
    TABLE_OF_CONTENTS = "table_of_contents"
    MAIN_CONTENT = "main_content"
    KEY_TAKEAWAYS = "key_takeaways"
    REFERENCES = "references"
    PRACTICAL_TASK = "practical_task"
    QUESTIONS = "questions"
    LEARNING_OUTCOMES = "learning_outcomes"
    APPENDIX = "appendix"


# Export Formats
class ExportFormat(str, Enum):
    """Supported export formats."""
    DOCX = "docx"
    PDF = "pdf"
    MARKDOWN = "markdown"


# Difficulty Levels
class DifficultyLevel(str, Enum):
    """Content difficulty levels."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


# Languages
class Language(str, Enum):
    """Supported languages."""
    ENGLISH = "en"
    RUSSIAN = "ru"


# Document Types
class DocumentType(str, Enum):
    """Types of documents."""
    LECTURE = "lecture"
    LAB_WORK = "lab_work"
    PRACTICAL_WORK = "practical_work"


# Default Configuration Values
DEFAULT_GROQ_MODEL = "mixtral-8x7b-32768"
DEFAULT_STORAGE_PATH = "./generated_documents"
DEFAULT_TEMPLATES_PATH = "./templates"
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_MAX_CONCURRENT_REQUESTS = 5
DEFAULT_MAX_BLOCKS_PER_DOCUMENT = 10
DEFAULT_MAX_TOKENS_PER_BLOCK = 8000
DEFAULT_LANGUAGE = Language.ENGLISH
DEFAULT_DIFFICULTY = DifficultyLevel.INTERMEDIATE
DEFAULT_EXPORT_FORMAT = ExportFormat.DOCX

# Block Generation Defaults
BLOCK_TYPE_TOKEN_LIMITS = {
    BlockType.TITLE_PAGE: 200,
    BlockType.INTRODUCTION: 1000,
    BlockType.TABLE_OF_CONTENTS: 500,
    BlockType.MAIN_CONTENT: 6000,
    BlockType.KEY_TAKEAWAYS: 800,
    BlockType.REFERENCES: 500,
    BlockType.PRACTICAL_TASK: 1500,
    BlockType.QUESTIONS: 800,
    BlockType.LEARNING_OUTCOMES: 500,
    BlockType.APPENDIX: 1000,
}

# Groq API Configuration
GROQ_TIMEOUT = 60
GROQ_MAX_RETRIES = 3
GROQ_RETRY_WAIT_SECONDS = 2  # Base wait for exponential backoff

# Document Generation
DEFAULT_DURATION_MINUTES = 90
DEFAULT_TEMPERATURE = 0.7

# String templates for prompts
SYSTEM_PROMPT_TEMPLATE = """You are an expert educator creating {language} educational content.
Your role is to generate high-quality {block_type} for {level} learners.
Maintain clarity, accuracy, and engagement.
Focus on pedagogical soundness while being accessible to your target audience."""

# File naming
DOCUMENT_ID_PREFIX = "doc_"
METADATA_SUFFIX = ".metadata.json"
LOG_SUFFIX = ".log"
