import json
import sys
from loguru import logger
import tempfile
import os



from .metadata_proccesor import create_metadata_from_ktp
from .folder_proccesor import create_folders
from .notes_proccesor import create_all_notes
from .arhivator import pack_and_copy_umk
from .gen_proccesor import gen_notes

def compose_umk(ktp_file_dir: str, output_file_path: str, discipline: str) -> str:
    logger.level("COMPOSE_UMK", no=10, color="<blue>")
    logger.log("COMPOSE_UMK","cтарт сборки УМК")

    with tempfile.TemporaryDirectory() as temp_dir:
        logger.log("COMPOSE_UMK", f"создана временная папка : {temp_dir}", )

        logger.log("COMPOSE_UMK", f"создаем мета данные из файла КТП", )
        create_metadata_from_ktp(temp_dir, ktp_file_dir, discipline)
        logger.log("COMPOSE_UMK", f"мета данные созданы", )


