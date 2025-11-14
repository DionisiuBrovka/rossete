import os
import random
from loguru import logger

from .ai_proccesor import *


def create_note_prop(t, settings, note):
    return f"""---
gen: "true"
tags:
  - {t}
Тема: {note['topic']}
Количество часов: {note['h']}
Номер занятия: {note['number']}
Состояние: Нужно усовершенствовать 
---"""


def create_note_from_metadata(
        settings : dict, 
        data : dict, 
        item_type : str, 
        get_item_name, 
        get_item_prop = None, 
        get_item_choise = None,
        get_item_promt = None):

    # собираем мета данные определенных типов
    items = []

    # выбираем записи из данных по типу 
    for item in data:
        if item['type'] == item_type:
            items.append(item)

    # фильтруем записи 
    if get_item_choise:
        items = get_item_choise(settings, items)

    # перебераем мета данные
    for n, item in enumerate(items):
        file_name = get_item_name(n, item)

        if os.path.exists(file_name):
            logger.log("CREATING_NOTES",f"пропускаем файл {file_name}, он уже создан")
            continue

        with open(f"{file_name}", "w+", encoding="UTF-8") as item_file:
            if get_item_prop:
                item_file.write(get_item_prop(settings, item))
                item_file.write("\n")
                item_file.write("\n")

            if get_item_promt:
                item_file.write("<promt>\n")
                item_file.write(get_item_promt(settings, item))
                item_file.write("\n")
                item_file.write("</promt>\n")
        
            logger.log("CREATING_NOTES",f"файл {file_name} создан")


def create_lection_notes(settings, data):
    create_note_from_metadata(
        settings,
        data,
        "лекция",
        get_item_name = lambda _n, _note: f"{settings['teoretical_part_path']}/Лекция №{_n+1}.md",
        get_item_prop=lambda _settings, _note: create_note_prop("Лекция", _settings, _note),
        get_item_promt=lambda _settings, _note: make_promt_lec(_note['title'], _note['h'], _settings['discipline']),
    )


def create_pract_notes(settings, data):
    create_note_from_metadata(
        settings,
        data,
        "лаба",
        get_item_name = lambda _n, _note: f"{settings['parctical_part_path']}/Лабораторная работа №{_n+1}.md",
        get_item_prop=lambda _settings, _note: create_note_prop("Лабораторная работа", _settings, _note),
        get_item_promt=lambda _settings, _note: make_promt_lab_n_prac(_note['title'], _note['h'], _settings['discipline'], "лабораторная работа"),
    )

    create_note_from_metadata(
        settings,
        data,
        "практос",
        get_item_name = lambda _n, _note: f"{settings['parctical_part_path']}/Практическая работа №{_n+1}.md",
        get_item_prop=lambda _settings, _note: create_note_prop("Практическая работа", _settings, _note),
        get_item_promt=lambda _settings, _note: make_promt_lab_n_prac(_note['title'], _note['h'], _settings['discipline'], "практическая работа"),
    )

def create_control_notes(settings, data):
    pass

def create_motivation_notes(settings, data):
    pass

def create_plan_notes(settings, data):
    pass


def create_all_notes(settings, data):
    logger.level("CREATING_NOTES", no=11, color="<white>")
    
    create_lection_notes(settings, data)
    create_pract_notes(settings, data)
    create_control_notes(settings, data)
    create_motivation_notes(settings, data)
    create_plan_notes(settings, data)
