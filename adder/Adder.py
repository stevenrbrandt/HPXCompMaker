from comp import *

@Component(namespace='adder')
class Adder:

    counter : int = 0
    values : smap[str, int] = default

    def get(self) -> int:
        "return counter;"

    def get_value(self, key : str) -> int:
        "return values[key];"

    def add(self, val : int) -> None:
        "counter += val;"

    def add_value(self, key : str, val : int) -> None:
        "values[key] += val;"
