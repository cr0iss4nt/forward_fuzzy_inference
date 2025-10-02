"""
Лабораторная работа №3 по дисциплине ЛОИС
Выполнена студентами группы 321702 Бураком Богданом Витальевичем, Семенидо Максимом Игоревичем, Мартыненко Константином Сергеевичем
Нечёткая логика
01.10.2025

Использованные материалы:
Голенков, В. В. Логические основы интеллектуальных систем. Практикум: учеб.-метод. пособие / В. В. Голенков. — БГУИР, 2011.
"""

from fuzzy_sets import FuzzySet

# вывести матрицу импликации
def print_implication_matrix(A: FuzzySet, B: FuzzySet, title="Матрица импликаций"):
    print(f"\n{title}: {A.name} -> {B.name}")
    x_elements = A.get_elements()
    y_elements = B.get_elements()

    corner = f"{A.name} \\ {B.name}"
    print(f"{corner:<10}", end=" ")
    for y in y_elements:
        print(f"{y:<8}", end=" ")
    print()

    for x in x_elements:
        print(f"{x:<10}", end=" ")
        for y in y_elements:
            impl_val = implication(A.get_value(x), B.get_value(y))
            print(f"{impl_val:<8.3f}", end=" ")
        print()
    print()

# вычисление t-нормы граничного произведения
def t_norm(value1, value2):
    return max(0, value1 + value2 - 1)

# вычисление импликации Лукасевича
def implication(value1, value2):
    return 1 if value1 <= value2 else 1 - value1 + value2

# шаг нечёткого логического вывода
def fuzzy_forward_inference(A: FuzzySet, B: FuzzySet, A_prime: FuzzySet, name):
    x_universe = A.get_elements()
    y_universe = B.get_elements()

    B_prime_dict = {}

    for y in y_universe:
        supremum_candidates = []
        for x in x_universe:
            implication_val = implication(A.get_value(x), B.get_value(y))
            t_norm_val = t_norm(A_prime.get_value(x), implication_val)
            supremum_candidates.append(round(t_norm_val, 3))
        B_prime_dict[y] = max(supremum_candidates) if supremum_candidates else 0.0

    #print_implication_matrix(A, B)

    return FuzzySet(f"{name}", B_prime_dict)

# нахождение всех пар множеств с одинаковым универсумом
def find_all_suitable_pairs(sets: list[FuzzySet]):
    return [(i.name, j.name) for i in sets for j in sets if i.get_elements() == j.get_elements()]