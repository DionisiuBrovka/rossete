"""
Rossete - Educational Content Generation MCP Server

Automates creation of educational content (lectures, lab work, practical work)
for universities using template-based generation and Groq API for ultra-fast
LLM inference.
"""

__version__ = "0.1.0"
__author__ = "Rossete Team"
__license__ = "MIT"

from .config import Config
from .exceptions import RossetException

__all__ = ["Config", "RossetException"]
