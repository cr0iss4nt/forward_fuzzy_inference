class FuzzySet:
    def __init__(self, name: str, data: dict[str, float]):
        self.name = name
        self.data = data

    def __str__(self):
        return '{' + ','.join([f"<{i},{j}>" for i, j in self.data.items()]) + '}'

    def get_value(self, element_name):
        return self.data[element_name]

    def get_elements(self):
        return sorted(self.data.keys())
