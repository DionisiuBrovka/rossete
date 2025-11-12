import os
import random
from loguru import logger

def create_note_from_metadata(
        settings : dict, 
        data : dict, 
        item_type : str, 
        get_name : function, 
        item_prop : function = None, 
        item_choise : function = None,
        promt :function  = None):
    logger.level("CREATING_NOTES", no=11, color="<green>")

    # собираем мета данные определенных типов
    items = []

    # выбираем записи из данных по типу 
    for item in data:
        if item['type'] == item_type:
            items.append(item)

    # фильтруем записи 
    if item_choise:
        items = item_choise(settings, items)

    # перебераем мета данные
    for n, item in enumerate(items):
        file_name = get_name(n, item)

        if os.path.exists(file_name):
            logger.log("CREATING_NOTES",f"пропускаем файл {file_name}, он уже создан")
            continue

        with open(f"{file_name}", "w+", encoding="UTF-8") as item_file:
            if item_prop:
                item_file.write(item_prop(settings, item))
                item_file.write("\n")

            if promt:
                item_file.write("<promt>\n")
                item_file.write(promt(settings, item))
                item_file.write("</promt>\n")
        
            logger.log("CREATING_NOTES",f"файл {file_name} создан")
