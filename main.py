from fuzzy_sets_interpreter import parse_fuzzy_set_file, parse_rules_file
from fuzzy_logic import forward_fuzzy_inference, find_all_a_prime


def is_repeating_set(a, sets):
    for i in sets:
        if i.data == a.data:
            return i.name
    return None


def main():
    # Загрузка нечётких множеств из файла
    try:
        fuzzy_sets = parse_fuzzy_set_file("data.txt")
        print("Загруженные нечёткие множества:")
        for fs in fuzzy_sets:
            print(f"{fs.name} = {fs}")
        print()
    except Exception as e:
        print(f"Ошибка при загрузке множеств: {e}")
        return

    # Загрузка правил из файла
    try:
        rules = parse_rules_file("rules.txt")
        print("Загруженные правила:")
        for left, right in rules:
            print(f"{left} ~> {right}")
        print()
    except Exception as e:
        print(f"Ошибка при загрузке правил: {e}")
        return

    # Список всех множеств (исходные + новые)
    all_sets = fuzzy_sets.copy()

    # Множество для отслеживания уже созданных комбинаций
    processed_combinations = []

    # Флаг для отслеживания появления новых множеств
    new_sets_created = True

    set_number = 1

    while new_sets_created:
        new_sets_created = False

        # Обновляем словарь множеств
        sets_by_name = {fs.name: fs for fs in all_sets}

        # Находим все возможные пары A и A' с одинаковыми универсумами
        a_prime_pairs = [i for i in find_all_a_prime(all_sets) if i not in processed_combinations]

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

                    B_prime = forward_fuzzy_inference(A, B, A_prime, f"I{set_number}")

                    print(f"{{ {A_prime.name}, {A.name} ~> {B.name}}} |~ I{set_number} = {B_prime}", end='')
                    repeats = is_repeating_set(B_prime, all_sets)

                    if repeats is None:
                        all_sets.append(B_prime)
                        new_sets_created = True
                    else:
                        print(f"={repeats}", end='')

                    print("")
                    set_number += 1


if __name__ == "__main__":
    main()