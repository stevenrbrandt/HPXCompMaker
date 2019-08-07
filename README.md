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
    def hello2() -> None:
        pass
    def write(self, s : str) -> None:
        cplusplus('std::cout << s << std::endl;')
    def __init__(self):
        cplusplus("/*comment*/")
    def __del__(self):
        pass
```
By using the magic of Python Decorators, running `Python PrintUtil.py` will generate the following two class files:

The first file is
[`PrintUtil.hpp`](https://github.com/stevenrbrandt/HPXCompMaker/blob/master/printutil/PrintUtil.hpp)

The second file is
[`PrintUtil_macros.hpp`](https://github.com/stevenrbrandt/HPXCompMaker/blob/master/printutil/PrintUtil_macros.cpp)

Note that all the Python types map to corresponding C++ types. `None` maps to
`Void`, `str` maps to `std::string`, and so on in a mostly intuitive manner.

Python's `__init__` function will become a constructor. In this case, it's an
empty constructor with a single comment inside.

Python's `__del__` function will become a destructor. In this case, it's
unimplemented. A separate C++ file will be required to provide its
implementation.

Likewise, the `hello2()` function, since it has no body, must be provided.
A file where those functions were provided by hand may be found here:
[`PrintUtil.cpp`](https://github.com/stevenrbrandt/HPXCompMaker/blob/master/printutil/PrintUtil.cpp)

See the printutil directory for a working Makefile and code example.

## A second example: Adder

Next, let us consider creating a component with state.

```
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
```

In this example, our component has two fields: counter, and values.
For values, we have type `smap[str,int]` which maps onto
`std::map<std::string,int>`. Note that we need to initialize it with
`default`, otherwise, our generated code will try to initialize it
with `nullptr`.

See the adder directory for a Makefile and working code example.
