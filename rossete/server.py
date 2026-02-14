"""
FastMCP server for Rossete.

Main entry point for MCP protocol integration.
"""

import logging
from typing import Any

from fastmcp import FastMCP

from .tools import document_tools, template_tools, utility_tools

logger = logging.getLogger(__name__)

# Create FastMCP app
app = FastMCP("Rossete")


@app.tool()
async def generate_document(
    template_id: str,
    topic: str,
    level: str = "intermediate",
    parameters: str = "{}",
) -> dict:
    """
    Generate an educational document from a template.

    Args:
        template_id: Template identifier (lecture_standard_v1, lab_work_v1, practical_work_v1)
        topic: Document topic
        level: Difficulty level (beginner, intermediate, advanced)
        parameters: JSON string with additional parameters

    Returns:
        Document generation result with file path and metadata
    """
    return await document_tools.generate_document(template_id, topic, level, parameters)


@app.tool()
def list_templates() -> dict:
    """
    List all available templates.

    Returns:
        List of available templates with metadata
    """
    return template_tools.list_templates()


@app.tool()
def get_template_details(template_id: str) -> dict:
    """
    Get detailed information about a template.

    Args:
        template_id: Template identifier

    Returns:
        Complete template definition and structure
    """
    return template_tools.get_template_details(template_id)


@app.tool()
def create_custom_template(
    name: str,
    document_type: str,
    blocks: str,
) -> dict:
    """
    Create a custom template for document generation.

    Args:
        name: Template name
        document_type: Type of document (lecture, lab_work, practical_work)
        blocks: JSON string with block configuration

    Returns:
        Template creation result
    """
    return template_tools.create_custom_template(name, document_type, blocks)


@app.tool()
def list_block_types() -> dict:
    """
    List all available block types that can be used in documents.

    Returns:
        List of block types with token limits
    """
    return utility_tools.list_block_types()


@app.tool()
def get_block_type_details(block_type: str) -> dict:
    """
    Get details about a specific block type.

    Args:
        block_type: Block type identifier

    Returns:
        Block type details and configuration
    """
    return utility_tools.get_block_type_details(block_type)


@app.tool()
def validate_parameters(template_id: str, parameters: str = "{}") -> dict:
    """
    Validate parameters for a template before generation.

    Args:
        template_id: Template identifier
        parameters: JSON string with parameters to validate

    Returns:
        Validation result
    """
    return utility_tools.validate_parameters(template_id, parameters)


@app.tool()
def export_document(document_id: str, format: str = "docx") -> dict:
    """
    Export a generated document to a different format.

    Args:
        document_id: Document identifier
        format: Export format (docx, pdf, markdown)

    Returns:
        Export status and file path
    """
    return document_tools.export_document(document_id, format)


@app.tool()
def get_document_status(document_id: str) -> dict:
    """
    Get status and metadata of a document.

    Args:
        document_id: Document identifier

    Returns:
        Document status and metadata
    """
    return document_tools.get_document_status(document_id)


@app.tool()
def get_server_info() -> dict:
    """
    Get server information and current configuration.

    Returns:
        Server version, configuration, and available resources
    """
    return utility_tools.get_server_info()


if __name__ == "__main__":
    import asyncio

    logger.info("Starting Rossete MCP Server")
    asyncio.run(app.run())
