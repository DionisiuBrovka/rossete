import sys
from loguru import logger
import utils

logger.remove()
logger.add(sys.stdout, colorize=True ,format="<green>{time:DD-MM HH:mm:ss}</green> | <lvl>{message}</lvl>")
utils.compose_umk("debug/АЛОВТ_КТП_основная часть.xlsx", "Арифметико-логические основы вычислительной техники")