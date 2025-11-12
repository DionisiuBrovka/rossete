import shutil
import os
from loguru import logger

def pack_and_copy_umk(temp_dir: str, output_dir: str, archive_name: str = "UMK_archive.zip") -> str:
    """
    Архивирует содержимое временной папки и копирует архив в указанную директорию.

    :param temp_dir: путь к временной папке (например, из tempfile.TemporaryDirectory)
    :param output_dir: путь к директории, куда нужно скопировать архив
    :param archive_name: имя создаваемого архива (по умолчанию 'UMK_archive.zip')
    :return: путь к итоговому архиву
    """
    logger.level("PACK_UMK", no=11, color="<cyan>")
    logger.log("PACK_UMK", f"начинается упаковка содержимого {temp_dir}")

    # Проверка путей
    if not os.path.exists(temp_dir):
        raise FileNotFoundError(f"Временная папка не найдена: {temp_dir}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Путь к временному архиву (внутри temp_dir)
    archive_path = os.path.join(temp_dir, archive_name)

    # Создаём архив
    shutil.make_archive(base_name=archive_path.replace(".zip", ""), format='zip', root_dir=temp_dir)
    logger.log("PACK_UMK", f"архив создан: {archive_path}")

    # Копируем в целевую папку
    final_path = os.path.join(output_dir, archive_name)
    shutil.copy2(archive_path, final_path)
    logger.log("PACK_UMK", f"архив скопирован в: {final_path}")

    return final_path
