from comp import *

@Component(namespace='adder')
class Adder:

    counter : int = 0
    values : smap[str, int] = default

    def get(self) -> int:
        cplusplus("return counter;")

    def get_value(self, key : str) -> int:
        cplusplus("return values[key];")

    def add(self, val : int) -> None:
        cplusplus("counter += val;")

    def add_value(self, key : str, val : int) -> None:
        cplusplus("values[key] += val;")
