from pathlib import Path
import re
import time

from loguru import logger
from .ai_proccesor import ask_ai

def find_files(root: str | Path, ext: str, case_sensitive: bool = False):
    root = Path(root)
    if not root.exists():
        return

    if not ext.startswith('.'):
        ext = '.' + ext

    for p in root.rglob('*'):
        if not p.is_file():
            continue
        file_ext = p.suffix  
        if case_sensitive:
            if file_ext == ext:
                yield p
        else:
            if file_ext.lower() == ext.lower():
                yield p


def extract_promt_text(file_path: str) -> str | None:
    """Извлекает текст между тегами <promt>...</promt> из файла."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Ошибка: файл '{file_path}' не найден.")
        return None

    match = re.search(r"<promt>(.*?)</promt>", content, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    else:
        print("Тег <promt>...</promt> не найден.")
        return None


def replace_promt_content(file_path: str, new_text: str) -> bool:
    """
    Открывает файл, находит тег <promt>...</promt> и заменяет его содержимое на new_text.
    Возвращает True, если замена выполнена успешно, иначе False.
    """
    try:
        with open(file_path, "r", encoding="UTF-8") as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Ошибка: файл '{file_path}' не найден.")
        return False

    updated_content = re.sub(
        r"<promt>.*?</promt>",
        f"{new_text}",
        content,
        flags=re.DOTALL | re.IGNORECASE
    )

    with open(file_path, "w", encoding="UTF-8") as file:
        file.write(updated_content)

    return True


def has_gen_true(file_path: str) -> bool:
    """Проверяет, есть ли в файле строка gen: "true"."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Ошибка: файл '{file_path}' не найден.")
        return False

    pattern = r'gen:\s*"true"'
    return bool(re.search(pattern, content, re.IGNORECASE))


def gen_notes(base_dir, settings, data):
    logger.level("CHEAK_NOTES", no=11, color="<white>")
    logger.level("GEN_NOTES", no=11, color="<yellow>")

    for note_path in find_files(base_dir, ".md"):
        logger.log("CHEAK_NOTES",f"проверяем файл: {note_path}")

        if has_gen_true(note_path):
            logger.log("GEN_NOTES",f"\t> файл отмечен для генерации")

            promt_text = extract_promt_text(note_path)
            logger.log("GEN_NOTES",f"\t> получен промт, длина - {len(promt_text)} символов")

            logger.log("GEN_NOTES",f"\t> генерим файл: {note_path}")
            try:
                replace_promt_content(note_path, ask_ai("vYhO2U1", promt_text))
                logger.log("GEN_NOTES",f"\t> Содержимое файла успешно обновлено.")
                time.sleep(10)
                logger.log("GEN_NOTES",f"\t> ✅ Генерация успешна")
            except:
                logger.log("GEN_NOTES",f"\t> ❌ ЯРЫК ПИЗДА РУЛЮ") 
                