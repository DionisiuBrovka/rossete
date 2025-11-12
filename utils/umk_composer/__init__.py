from loguru import logger
import tempfile
import os

from .metadata_proccesor import create_metadata_from_ktp, load_metadata

def compose_umk(ktp_file_dir: str, discipline: str) -> str:
    logger.level("COMPOSE_UMK", no=10, color="<white>")
    logger.log("COMPOSE_UMK","cтарт сборки УМК")

    with tempfile.TemporaryDirectory() as temp_dir:
        logger.log("COMPOSE_UMK", f"создана временная папка : {temp_dir}", )

        logger.log("COMPOSE_UMK", f"создаем мета данные из файла КТП", )
        create_metadata_from_ktp(temp_dir, ktp_file_dir, discipline)
        logger.log("COMPOSE_UMK", f"мета данные созданы", )
        settings, data = load_metadata(temp_dir)
        logger.log("COMPOSE_UMK", f"загружаем мета данные", )

