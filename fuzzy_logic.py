"""
Лабораторная работа №3 по дисциплине ЛОИС
Выполнена студентами группы 321702 Бураком Богданом Витальевичем, Семенидо Максимом Игоревичем, Мартыненко Константином Сергеевичем
Нечёткая логика
30.09.2025

Использованные материалы:
Голенков, В. В. Логические основы интеллектуальных систем. Практикум: учеб.-метод. пособие / В. В. Голенков. — БГУИР, 2011.
"""

from fuzzy_sets import FuzzySet


def t_norm(value1, value2):
    return max(0, value1 + value2 - 1)

def implication(value1, value2):
    return 1 if value1 <= value2 else 1 - value1 + value2

def forward_fuzzy_inference(A: FuzzySet, B: FuzzySet, A_prime: FuzzySet, name):
    x_universe = A.get_elements()
    y_universe = B.get_elements()

    B_prime_dict = {}

    for y in y_universe:
        supremum_candidates = []
        for x in x_universe:
            implication_val = implication(A.get_value(x), B.get_value(y))
            t_norm_val = t_norm(A_prime.get_value(x), implication_val)
            supremum_candidates.append(t_norm_val)
        B_prime_dict[y] = max(supremum_candidates) if supremum_candidates else 0.0

    return FuzzySet(f"{name}", B_prime_dict)

def find_all_suitable_pairs(sets: list[FuzzySet]):
    return [(i.name, j.name) for i in sets for j in sets if i.get_elements() == j.get_elements()]