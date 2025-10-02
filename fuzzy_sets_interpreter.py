"""
Лабораторная работа №3 по дисциплине ЛОИС
Выполнена студентами группы 321702 Бураком Богданом Витальевичем, Семенидо Максимом Игоревичем, Мартыненко Константином Сергеевичем
Парсинг нечётких множеств и правил
30.09.2025

Использованные материалы:
Голенков, В. В. Логические основы интеллектуальных систем. Практикум: учеб.-метод. пособие / В. В. Голенков. — БГУИР, 2011.
"""

from fuzzy_sets import *

# преобразование строки в нечёткое множество
def parse_fuzzy_set(input_string: str) -> FuzzySet:
    parts = input_string.split('=', 1)
    if len(parts) != 2:
        raise ValueError("Invalid format: expected 'name = {data}'")

    name = parts[0].strip()

    data_part = parts[1].strip()
    if not data_part.startswith('{') or not data_part.endswith('}'):
        raise ValueError("Invalid format: data must be enclosed in curly braces")

    data_content = data_part[1:-1].strip()
    if data_content == '':
        return FuzzySet(name, {})

    data = {}

    elements = data_content.split('>,')

    for element in elements:
        element = element.strip()
        if element.startswith('<'):
            element = element[1:]
        if element.endswith('>'):
            element = element[:-1]

        key_value = element.split(',', 1)
        if len(key_value) != 2:
            raise ValueError(f"Invalid element format: {element}")

        key = key_value[0].strip()
        value_str = key_value[1].strip()

        try:
            value = float(value_str)
        except ValueError:
            raise ValueError(f"Invalid value format: {value_str}")

        data[key] = round(value, 3)

    return FuzzySet(name, data)

# парсинг нечётких множеств из файла
def parse_fuzzy_set_file(filename) -> list[FuzzySet]:
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
        sets = [parse_fuzzy_set(line) for line in lines]
        return sets

# парсинг правил из файла
def parse_rules_file(filename) -> list[tuple[str, str]]:
    tuples_list = []

    with open(filename) as file:
        for line in file:
            line = line.strip()
            if line:
                try:
                    left, right = line.split('~>')
                    tuples_list.append((left.strip(), right.strip()))
                except ValueError:
                    print(f"Skipping invalid line: {line}")

    return tuples_list