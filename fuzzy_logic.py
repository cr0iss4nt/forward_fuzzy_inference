from fuzzy_sets import FuzzySet


def t_norm(value1, value2):
    # lukasiewicz
    # return max(0, value1 + value2 - 1)

    # goedel
    return min(value1, value2)

def implication(value1, value2):
    # lukasiewicz
    # return 1 if value1 <= value2 else 1 - value1 + value2

    # goedel
    return 1 if value1 <= value2 else value2

def forward_fuzzy_inference(A: FuzzySet, B: FuzzySet, A_prime: FuzzySet, name):
    """
    Прямой нечёткий вывод с использованием импликации Гёделя и t-нормы минимума.

    Параметры:
        A: dict - Нечёткое множество A (ключи - элементы универсума, значения - степени принадлежности).
        B: dict - Нечёткое множество B (аналогично A).
        A_prime: dict - Нечёткое множество A' (аналогично A).

    Возвращает:
        dict - Нечёткое множество B' (ключи - элементы универсума B, значения - вычисленные степени принадлежности).
    """
    # Универсумы для x и y
    x_universe = A.get_elements()
    y_universe = B.get_elements()

    B_prime_dict = {}

    for y in y_universe:
        supremum_candidates = []
        for x in x_universe:
            # Вычисляем импликацию A(x) ~> B(y)
            implication_val = implication(A.get_value(x), B.get_value(y))
            # Применяем t-норму к A'(x) и результату импликации
            t_norm_val = t_norm(A_prime.get_value(x), implication_val)
            supremum_candidates.append(t_norm_val)
        # Супремум - максимальное значение
        B_prime_dict[y] = max(supremum_candidates) if supremum_candidates else 0.0

    return FuzzySet(f"{name}", B_prime_dict)

def find_all_a_prime(sets: list[FuzzySet]):
    return [(i.name, j.name) for i in sets for j in sets if i.get_elements() == j.get_elements()]