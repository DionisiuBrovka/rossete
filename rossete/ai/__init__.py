"""
AI integration module for Rossete.

Handles integration with Groq API and other LLM providers.
"""

from .groq_client import GroqClient, get_groq_client

__all__ = ["GroqClient", "get_groq_client"]
