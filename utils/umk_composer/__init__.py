from loguru import logger
import tempfile
import os



from .metadata_proccesor import create_metadata_from_ktp, load_metadata
from .folder_proccesor import create_folders
from .notes_proccesor import create_lection_notes
from .arhivator import pack_and_copy_umk

def compose_umk(ktp_file_dir: str, discipline: str) -> str:
    logger.level("COMPOSE_UMK", no=10, color="<white>")
    logger.log("COMPOSE_UMK","cтарт сборки УМК")

    with tempfile.TemporaryDirectory() as temp_dir:
        logger.log("COMPOSE_UMK", f"создана временная папка : {temp_dir}", )

        logger.log("COMPOSE_UMK", f"создаем мета данные из файла КТП", )
        create_metadata_from_ktp(temp_dir, ktp_file_dir, discipline)
        logger.log("COMPOSE_UMK", f"мета данные созданы", )

        logger.log("COMPOSE_UMK", f"загружаем мета данные", )
        settings, data = load_metadata(temp_dir)
        logger.log("COMPOSE_UMK", f"мета данные загружены", )

        logger.log("COMPOSE_UMK", f"создаем папки", )
        create_folders(temp_dir, settings)
        logger.log("COMPOSE_UMK", f"папки созданы", )

        logger.log("COMPOSE_UMK", f"создаем заметки лекций", )
        create_lection_notes(settings, data)
        logger.log("COMPOSE_UMK", f"заметки лекций созданы", )

        pack_and_copy_umk(temp_dir, "/home/home-pc/Desktop")


