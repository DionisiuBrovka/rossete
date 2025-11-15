import json
import os
from loguru import logger

from .excel_proccesor import excel_to_structure


def make_folders_metadata(base_dir):
    folders_metadata = {}

    folders_metadata['base'] = f"{base_dir}"
    folders_metadata['teoretical_part_path'] = f"{base_dir}/1 Теоретический раздел"
    folders_metadata['parctical_part_path'] = f"{base_dir}/2 Практический раздел"
    folders_metadata['control_part_path'] = f"{base_dir}/3 Раздел контроля знаний"
    folders_metadata['help_part_path'] = f"{base_dir}/4 Вспомогательный раздел"
    folders_metadata['low_part_path'] = f"{base_dir}/5 Работа с низкомотивироваными учащимися"
    folders_metadata['high_part_path'] = f"{base_dir}/6 Работа с высокомотивироваными учащимися"
    folders_metadata['extra_part_path'] = f"{base_dir}/7 Дополнительные материалы"
    folders_metadata['plans_path'] = f"{base_dir}/7 Дополнительные материалы/Планы занятий"

    return folders_metadata


def make_topics_metadata(items):
    topics_metadata = []

    i = 1
    for item in items['data']:
        if item['type'] == "раздел":
            item['id'] = i
            topics_metadata.append(item)
            i += 1

    return topics_metadata


def make_chapters_metadata(items):
    chapters_metadata = []

    i = 1
    for item in items['data']:
        if item['type'] == "тема":
            item['id'] = i
            chapters_metadata.append(item)
            i += 1

    return chapters_metadata


def make_lessons_metadata(items, chapters_metadata, topics_metadata):
    lessons_metadata = {}

    return lessons_metadata


def make_notes_metadata(items):
    notes_metadata = {}

    return notes_metadata


def create_metadata_from_ktp(base_dir, ktp_file_path, discipline):
    logger.level("CREATE_METADATA", no=11, color="<white>")
    
    if not os.path.exists(ktp_file_path):
        logger.error("Файл КТП не найден")
        raise Exception("Файл КТП не найден")


    logger.log("CREATE_METADATA", f"парсим файл КТП : {ktp_file_path}")
    items = excel_to_structure(ktp_file_path, sheet_name=0)

    folders_metadata = make_folders_metadata(base_dir),

    chapters_metadata = make_chapters_metadata(items)
    topics_metadata = make_topics_metadata(items)

    lessons_metadata = make_lessons_metadata(items, chapters_metadata, topics_metadata)
    notes_metadata = make_notes_metadata(lessons_metadata, folders_metadata)

    meta = {
        "discipline": discipline,
        "folders" : folders_metadata, 
        "notes" : notes_metadata,
    }

    logger.log("CREATE_METADATA", f"созданы метаданные \n{json.dumps(meta, indent=2, ensure_ascii=False)}")

    with open(f'{base_dir}/meta.json', "w+", encoding="UTF-8") as meta_file:
        json.dump(meta, meta_file, ensure_ascii=False, indent=4)
        logger.log("CREATE_METADATA", f"сохранили мета данные в файл : {f'{base_dir}/meta.json'}")
