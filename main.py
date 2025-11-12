import sys
from loguru import logger
from interfaces.cli import cli

logger.remove()
logger.add(sys.stdout, colorize=True ,format="<green>{time:DD-MM HH:mm:ss}</green> | <lvl>{message}</lvl>")

if __name__ == '__main__':
    cli()