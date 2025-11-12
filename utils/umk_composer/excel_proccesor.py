import os

from typing import Optional, Dict, Any, List
import re
import json

def roman_to_int(s: str) -> Optional[int]:
    if not s:
        return None
    s = s.upper().strip()
    roman_map = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}
    i = 0
    total = 0
    try:
        while i < len(s):
            if i+1 < len(s) and roman_map[s[i]] < roman_map[s[i+1]]:
                total += roman_map[s[i+1]] - roman_map[s[i]]
                i += 2
            else:
                total += roman_map[s[i]]
                i += 1
        return total
    except KeyError:
        return None


def _to_int_safe(x):
    try:
        if x is None:
            return None
        if isinstance(x, (int, float)) and not (isinstance(x, float) and (x != x)):
            return int(x)
        s = str(x).strip()
        if s == '':
            return None
        return int(float(s))
    except Exception:
        return None


def excel_to_structure(path: str, sheet_name=0) -> Dict[str, Any]:
    """
    Читает Excel-файл и возвращает словарь {"data": [...]} в нужной структуре.
    """
    import pandas as pd

    df = pd.read_excel(path, sheet_name=sheet_name, dtype=str, header=0)

    # Определяем нужные колонки
    cols = {c.strip().lower(): c for c in df.columns}
    col_num = col_title = col_hours = None
    for k, orig in cols.items():
        if "№" in k or "номер" in k:
            col_num = orig
        if "наименован" in k or "тем" in k or "раздел" in k:
            col_title = orig
        if "час" in k:
            col_hours = orig

    all_cols = list(df.columns)
    if col_title is None and len(all_cols) >= 2:
        col_title = all_cols[1]
    if col_num is None and len(all_cols) >= 1:
        col_num = all_cols[0]
    if col_hours is None and len(all_cols) >= 3:
        col_hours = all_cols[2]

    data_out: List[Dict[str, Any]] = []
    current_chapter = None
    last_subchapter = None
    last_subtopic = None
    id_counter = 1

    re_sub = re.compile(r'^\s*(\d+)\s*\.\s*(\d+)\b')
    re_chapter_arb = re.compile(r'Раздел\s+(\d+)', re.I)
    re_chapter_roman = re.compile(r'Раздел\s+([IVXLCDM]+)', re.I)
    re_section_prefix = re.compile(r'^\s*Раздел', re.I)
    re_lab = re.compile(r'лаборат', re.I)
    re_prac = re.compile(r'рактическа', re.I)
    re_control = re.compile(r'контрольн|обязательн', re.I)
    re_total = re.compile(r'ИТОГО', re.I)

    for _, row in df.iterrows():
        raw_num = row.get(col_num)
        raw_title = row.get(col_title)
        raw_hours = row.get(col_hours)
        title = str(raw_title).strip() if raw_title else ""

        if title == "" or re_total.search(title):
            continue
        h = _to_int_safe(raw_hours)

        # Раздел
        if re_section_prefix.search(title) or re_chapter_arb.search(title) or re_chapter_roman.search(title):
            m_arb = re_chapter_arb.search(title)
            if m_arb:
                current_chapter = int(m_arb.group(1))
            else:
                m_roman = re_chapter_roman.search(title)
                if m_roman:
                    current_chapter = roman_to_int(m_roman.group(1))
            last_subchapter = None
            last_subtopic = None

            data_out.append({
                "id": id_counter,
                "type": "раздел",
                "title": title
            })
            id_counter += 1
            continue

        # Подраздел (1.1, 2.3 и т.д.)
        msub = re_sub.search(title)
        if msub:
            last_subchapter = int(msub.group(1))
            last_subtopic = int(msub.group(2))
            data_out.append({
                "id": id_counter,
                "type": "тема",
                "title": title
            })
            id_counter += 1
            continue

        # Лабораторная
        if re_lab.search(title):
            number = _to_int_safe(raw_num)
            entry = {
                "id": id_counter,
                "type": "лаба",
                "title": title,
                "chapter": last_subchapter or current_chapter,
                "topic": last_subtopic,
                "number": number,
                "h": h
            }
            data_out.append(entry)
            id_counter += 1
            continue

        # Практическая
        if re_prac.search(title):
            number = _to_int_safe(raw_num)
            entry = {
                "id": id_counter,
                "type": "практос",
                "title": title,
                "chapter": last_subchapter or current_chapter,
                "topic": last_subtopic,
                "number": number,
                "h": h
            }
            data_out.append(entry)
            id_counter += 1
            continue

        # Контрольная/ОКР
        if re_control.search(title):
            number = _to_int_safe(raw_num)
            entry = {
                "id": id_counter,
                "type": "окр",
                "title": title,
                "chapter": last_subchapter or current_chapter,
                "topic": last_subtopic,
                "number": number,
                "h": h
            }
            data_out.append(entry)
            id_counter += 1
            continue

        # Лекция
        num_val = _to_int_safe(raw_num)
        if num_val is not None:
            entry = {
                "id": id_counter,
                "type": "лекция",
                "title": title,
                "chapter": last_subchapter or current_chapter,
                "topic": last_subtopic,
                "number": num_val,
                "h": h
            }
            data_out.append(entry)
            id_counter += 1
            continue

        # Прочий текст
        data_out.append({
            "id": id_counter,
            "type": "текст",
            "title": title
        })
        id_counter += 1
    return {"data": data_out}