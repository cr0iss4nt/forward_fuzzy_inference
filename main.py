"""
Лабораторная работа №3 по дисциплине ЛОИС
Выполнена студентами группы 321702 Бураком Богданом Витальевичем, Семенидо Максимом Игоревичем, Мартыненко Константином Сергеевичем
Главный файл приложения
30.09.2025

Использованные материалы:
Голенков, В. В. Логические основы интеллектуальных систем. Практикум: учеб.-метод. пособие / В. В. Голенков. — БГУИР, 2011.
"""

from fuzzy_sets_interpreter import parse_fuzzy_set_file, parse_rules_file
from fuzzy_logic import forward_fuzzy_inference, find_all_suitable_pairs


def find_duplicate(new_set, all_sets):
    for fs in all_sets:
        if fs.data == new_set.data:
            return fs.name
    return None


def main():
    try:
        fuzzy_sets = parse_fuzzy_set_file("data.txt")
    except Exception as e:
        print(f"Sets loading error: {e}")
        return

    try:
        rules = parse_rules_file("rules.txt")
    except Exception as e:
        print(f"Rules loading error: {e}")
        return

    all_sets = fuzzy_sets.copy()
    processed_combinations = set()
    set_number = 1

    while True:
        sets_by_name = {fs.name: fs for fs in all_sets}
        new_sets_found = False

        for a_name, a_prime_name in find_all_suitable_pairs(all_sets):
            if (a_name, a_prime_name) in processed_combinations:
                continue
            processed_combinations.add((a_name, a_prime_name))

            for left, right in rules:
                if left != a_name or right not in sets_by_name:
                    continue

                A = sets_by_name[a_name]
                B = sets_by_name[right]
                A_prime = sets_by_name[a_prime_name]

                B_prime = forward_fuzzy_inference(A, B, A_prime, f"I{set_number}")

                print(f"{{ {A_prime.name}, {A.name} ~> {B.name}}} |~ I{set_number} = {B_prime}", end='')

                duplicate_name = find_duplicate(B_prime, all_sets)
                if duplicate_name is None:
                    all_sets.append(B_prime)
                    new_sets_found = True
                else:
                    print(f"={duplicate_name}", end='')

                print()
                set_number += 1

        if not new_sets_found:
            break


if __name__ == "__main__":
    main()
