import os

from loguru import logger


def create_folders(base_dir, settings):
    logger.level("CREATING_FOLDERS", no=11, color="<green>")

    settings['teoretical_part_path'] = f"{base_dir}/1 Теоретический раздел"
    settings['parctical_part_path'] = f"{base_dir}/2 Практический раздел"
    settings['control_part_path'] = f"{base_dir}/3 Раздел контроля знаний"
    settings['help_part_path'] = f"{base_dir}/4 Вспомогательный раздел"
    settings['low_part_path'] = f"{base_dir}/5 Работа с низкомотивироваными учащимися"
    settings['high_part_path'] = f"{base_dir}/6 Работа с высокомотивироваными учащимися"
    settings['extra_part_path'] = f"{base_dir}/7 Дополнительные материалы"
    settings['plans'] = f"{base_dir}/7 Дополнительные материалы/Планы занятий"

    os.mkdir(settings['teoretical_part_path'])
    logger.log("CREATING_FOLDERS",f"папка {settings['teoretical_part_path']} создана")

    os.mkdir(settings['parctical_part_path'])
    logger.log("CREATING_FOLDERS",f"папка {settings['parctical_part_path']} создана")

    os.mkdir(settings['control_part_path'])
    logger.log("CREATING_FOLDERS",f"папка {settings['control_part_path']} создана")

    os.mkdir(settings['help_part_path'])
    logger.log("CREATING_FOLDERS",f"папка {settings['help_part_path']} создана")

    os.mkdir(settings['low_part_path'])
    logger.log("CREATING_FOLDERS",f"папка {settings['low_part_path']} создана")

    os.mkdir(settings['high_part_path'])
    logger.log("CREATING_FOLDERS",f"папка {settings['high_part_path']} создана")

    os.mkdir(settings['extra_part_path'])
    logger.log("CREATING_FOLDERS",f"папка {settings['extra_part_path']} создана")

    os.mkdir(settings['plans'])
    logger.log("CREATING_FOLDERS",f"папка {settings['plans']} создана")

