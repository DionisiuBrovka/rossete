"""
Concrete block implementations for Rossete.
"""

from .appendix import AppendixBlock
from .introduction import IntroductionBlock
from .key_takeaways import KeyTakeawaysBlock
from .learning_outcomes import LearningOutcomesBlock
from .main_content import MainContentBlock
from .practical_task import PracticalTaskBlock
from .questions import QuestionsBlock
from .references import ReferencesBlock
from .title_page import TitlePageBlock

__all__ = [
    "TitlePageBlock",
    "IntroductionBlock",
    "MainContentBlock",
    "KeyTakeawaysBlock",
    "ReferencesBlock",
    "PracticalTaskBlock",
    "QuestionsBlock",
    "LearningOutcomesBlock",
    "AppendixBlock",
]
