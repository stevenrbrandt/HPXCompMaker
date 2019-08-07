from comp import *

@Component(namespace='printutil')
class PrintUtil:
    def hello(self) -> None:
        cplusplus('std::cout << "Hello" << std::endl;')
    def hello2() -> None:
        pass
    def write(self, s : str) -> None:
        cplusplus('std::cout << s << std::endl;')
    def __init__(self):
        cplusplus("/*comment*/")
    def __del__(self):
        pass
