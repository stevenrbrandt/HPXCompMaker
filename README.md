# The HPX Component Maker

The idea behind this project is to write a simple Python class definition
and have it generate all the necessary boilerplate for a full HPX component.

## A first example...

Suppose we create a class named `PrintUtil.py` as follows:
```
  from comp import *

  @Component(namespace='printutil')
  class PrintUtil:
      def hello(self) -> None:
          cplusplus('std::cout << "Hello" << std::endl;')
      def write(self, s : str) -> None:
          cplusplus('std::cout << s << std::endl;')
      def __init__(self):
          cplusplus("/*comment*/")
```
By using the magic of Python Decorators, running `Python PrintUtil.py` will generate the following two class files:

The first file is
[`PrintUtil.hpp`](https://github.com/stevenrbrandt/HPXCompMaker/blob/master/PrintUtil.hpp)

The second file is
[`PrintUtil_macros.hpp`](https://github.com/stevenrbrandt/HPXCompMaker/blob/master/PrintUtil_macros.hpp)
