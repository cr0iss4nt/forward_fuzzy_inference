from fuzzy_sets import *

# How it's supposed to be viewed:
"""
A = {<a, 0.5>, <b, 1>, <c, 0>}
B = {<e, 0.3>, <b, 0.1>, <n, 0.95>}
"""


def parse_fuzzy_set(input_string: str) -> FuzzySet:
    """
    Parse a string in the format "A = {<a, 0.5>, <b, 1>, <c, 0>}" and return a FuzzySet object.
    """
    # Split the string to separate the name from the data part
    parts = input_string.split('=', 1)
    if len(parts) != 2:
        raise ValueError("Invalid format: expected 'name = {data}'")

    name = parts[0].strip()

    data_part = parts[1].strip()
    if not data_part.startswith('{') or not data_part.endswith('}'):
        raise ValueError("Invalid format: data should be enclosed in curly braces")

    # Remove the outer curly braces
    data_content = data_part[1:-1].strip()
    if data_content == '':
        return FuzzySet(name, {})

    # Parse the individual elements
    data = {}

    # Split by '>, ' to separate the elements, but be careful with the last one
    elements = data_content.split('>,')

    for element in elements:
        element = element.strip()
        # Remove any remaining angle brackets
        if element.startswith('<'):
            element = element[1:]
        if element.endswith('>'):
            element = element[:-1]

        # Split by comma to separate the key and value
        key_value = element.split(',', 1)
        if len(key_value) != 2:
            raise ValueError(f"Invalid element format: {element}")

        key = key_value[0].strip()
        value_str = key_value[1].strip()

        try:
            value = float(value_str)
        except ValueError:
            raise ValueError(f"Invalid value format: {value_str}")

        data[key] = value

    return FuzzySet(name, data)

def parse_fuzzy_set_file(filename) -> list[FuzzySet]:
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
        sets = [parse_fuzzy_set(line) for line in lines]
        return sets

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