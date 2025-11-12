import json
import os
from loguru import logger

from .excel_proccesor import excel_to_structure

def create_metadata_from_ktp(base_dir, ktp_file_path, discipline):
    logger.level("CREATE_METADATA", no=11, color="<green>")
    
    if not os.path.exists(ktp_file_path):
        logger.error("Файл КТП не найден")
        raise Exception("Файл КТП не найден")


    logger.log("CREATE_METADATA", f"парсим файл КТП : {ktp_file_path}")
    items = excel_to_structure(ktp_file_path, sheet_name=0)

    meta = {
        "settings" : {
            "discipline": discipline
        }
    }
    
    meta['data'] = items['data']


    logger.log("CREATE_METADATA", f"мета данные : \n{json.dumps(meta, ensure_ascii=False, indent=2)}")

    with open(f'{base_dir}/meta.json', "w+", encoding="UTF-8") as meta_file:
        json.dump(meta, meta_file, ensure_ascii=False, indent=4)
        logger.log("CREATE_METADATA", f"сохранили мета данные в файл : {f'{base_dir}/meta.json'}")


def load_metadata(base_dir):
    logger.level("LOAD_METADATA", no=11, color="<green>")

    metadata_path = f"{base_dir}/meta.json"

    if not os.path.exists(base_dir):
        logger.error("Файл мета данных не найден")
        raise Exception("Файл мета данных не найден")
    
    logger.log("LOAD_METADATA", "загружаем мета данные из : {metadata_path}")
    

    with open(metadata_path, "r+", encoding="UTF-8") as meta_file:
        meta_data = json.load(meta_file)

        setting = meta_data['settings']
        logger.log("LOAD_METADATA", f"Загружены настройки:")
        logger.log("LOAD_METADATA", f"\n{json.dumps(setting, ensure_ascii=False, indent=2)}")

        data = meta_data['data']
        logger.log("LOAD_METADATA", "Загружены данные:")
        logger.log("LOAD_METADATA", f"Загружены данные: всего {len(data)} записей") 

        return setting, data