"""
Лабораторная работа №3 по дисциплине ЛОИС
Выполнена студентами группы 321702 Бураком Богданом Витальевичем, Семенидо Максимом Игоревичем, Мартыненко Константином Сергеевичем
Главный файл приложения
01.10.2025

Использованные материалы:
Голенков, В. В. Логические основы интеллектуальных систем. Практикум: учеб.-метод. пособие / В. В. Голенков. — БГУИР, 2011.
"""

from fuzzy_sets_interpreter import parse_fuzzy_set_file, parse_rules_file
from fuzzy_logic import fuzzy_forward_inference, find_all_suitable_pairs, print_implication_matrix


# поиск множества, которое это множество повторяет
def is_repeating_set(a, sets):
    for i in sets:
        if i.data == a.data:
            return i.name
    return None


def main():
    try:
        fuzzy_sets = parse_fuzzy_set_file("data.txt")
        print("Загруженные нечёткие множества:")
        for fs in fuzzy_sets:
            print(f"{fs.name} = {fs}")
        print()
    except Exception as e:
        print(f"Ошибка при загрузке множеств: {e}")
        return

    try:
        rules = parse_rules_file("rules.txt")
        print("Загруженные правила:")
        for left, right in rules:
            print(f"{left} ~> {right}")
        print()
    except Exception as e:
        print(f"Ошибка при загрузке правил: {e}")
        return

    all_sets = fuzzy_sets.copy()

    processed_combinations = []

    new_sets_created = True

    set_number = 1

    sets_by_name = {fs.name: fs for fs in all_sets}
    for i,j in rules:
        print_implication_matrix(sets_by_name[i], sets_by_name[j])

    while new_sets_created:
        new_sets_created = False

        sets_by_name = {fs.name: fs for fs in all_sets}

        # список пар, которые можно обработать
        a_prime_pairs = [i for i in find_all_suitable_pairs(all_sets) if i not in processed_combinations]

        for a_name, a_prime_name in a_prime_pairs:
            combination_key = (a_name, a_prime_name)
            if combination_key in processed_combinations:
                continue

            processed_combinations.append(combination_key)

            for left, right in rules:
                if left == a_name and right in sets_by_name:
                    A = sets_by_name[a_name]
                    B = sets_by_name[right]

                    A_prime = sets_by_name[a_prime_name]

                    # шаг нечёткого логического вывода
                    new_set_name = f"I{set_number}"
                    B_prime = fuzzy_forward_inference(A, B, A_prime, new_set_name)

                    print(f"{{ {A_prime.name}, {A.name} ~> {B.name}}} |~ {new_set_name} = {B_prime}", end='')

                    # проверка, повторяет ли получившееся множество уже имеющееся
                    repeats = is_repeating_set(B_prime, all_sets)
                    if repeats is None:
                        all_sets.append(B_prime)
                        new_sets_created = True
                    else:
                        print(f"={repeats}", end='')

                    print("")
                    set_number += 1
        #print("="*100)

if __name__ == "__main__":
    main()