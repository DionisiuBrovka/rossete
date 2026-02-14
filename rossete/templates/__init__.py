"""
Template system for Rossete.

Manages template definitions for document generation.
"""

from .registry import TemplateRegistry, get_template_registry

__all__ = ["TemplateRegistry", "get_template_registry"]
