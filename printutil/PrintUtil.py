from comp import *

@Component(namespace='printutil',pybind11='prutil')
class PrintUtil:
    def hello(self) -> None:
        'std::cout << "Hello" << std::endl;'
    def hello2(self) -> None:
        pass
    def write(self, s : str) -> None:
        'std::cout << s << std::endl;'
    def one(self) -> int:
        "return 1;"
    def __init__(self):
        "/*comment*/"
    def __del__(self):
        pass
