import os
import random


def create_note_from_metadata(
        settings, 
        data, 
        item_type, 
        get_name, 
        make_item_prop, 
        make_rnd=False, 
        promt=None):
    # собираем мета данные определенных типов
    items = []
    for item in data:
        if item['type'] == item_type:
            items.append(item)

    if make_rnd:
        random.shuffle(items)
        items = items[:len(items)//2]

    # перебераем мета данные
    for n, item in enumerate(items):
        file_name = get_name(n, item)

        if os.path.exists(file_name):
            print(f"> Файл \"{file_name}\" уже создан")
            continue

        with open(f"{file_name}", "w+", encoding="UTF-8") as item_file:
            item_file.write(make_item_prop(settings, item))
            item_file.write("\n")
            if promt:
                item_file.write("<promt>\n")
                item_file.write(promt(settings, item))
                item_file.write("</promt>\n")
            print(f"> Файл \"{file_name}\" создан")