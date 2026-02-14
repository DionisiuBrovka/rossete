"""
Entry point for running Rossete as a module.

Usage: python -m rossete
"""

import asyncio
import logging

from .config import get_config
from .server import app

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


async def main():
    """Main entry point."""
    try:
        config = get_config()
        config.ensure_directories_exist()
        logger.info("Starting Rossete MCP Server")
        logger.info(f"Using Groq model: {config.groq_model}")
        logger.info(f"Storage path: {config.get_storage_path()}")
        logger.info(f"Templates path: {config.get_templates_path()}")
        await app.run()
    except Exception as e:
        logger.error(f"Failed to start server: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    asyncio.run(main())
