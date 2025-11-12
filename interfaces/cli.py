import time
from utils import umk_composer

# compose_umk("debug/АЛОВТ_КТП_основная часть.xlsx", "/home/home-pc/Desktop", "Арифметико-логические основы вычислительной техники")

import click

@click.group()
def cli():
    """Rossete - ИИ инструменты для преподователя"""
    pass

@cli.command()
@click.option("--ktp_file", prompt="Полный путь к КТП", help="полный путь к таблице с КТП")
@click.option("--output_dir", prompt="Путь для сохранения готового УМК", help="полный путь к папке для сохранения")
@click.option("--discipline", prompt="Название предмета", help="название предмета")
def compose_umk(ktp_file:str, output_dir:str, discipline:str):
    """Генерация УМК из таблицы КТП"""
    print()
    time.sleep(1)
    print()
    umk_composer.compose_umk(ktp_file, output_dir, discipline)