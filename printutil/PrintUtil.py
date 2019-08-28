from comp import *

@Component(namespace='printutil',pybind11='prutil')
class PrintUtil:
    def hello(self) -> None:
        cplusplus('std::cout << "Hello" << std::endl;')
    def hello2(self) -> None:
        pass
    def write(self, s : str) -> None:
        cplusplus('std::cout << s << std::endl;')
    def one(self) -> int:
        cplusplus("return 1;")
    def __init__(self):
        cplusplus("/*comment*/")
    def __del__(self):
        pass
