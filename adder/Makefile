HPX_LIB_DIR=/usr/local/lib64

run: main
	LD_LIBRARY_PATH=.:$(HPX_LIB_DIR) ./main 

Adder.hpp Adder_macros.cpp : Adder.py
	python3 Adder.py

Adder_macros.o : Adder_macros.cpp Adder.hpp
	hpxcxx -fPIC -g -c -I. Adder_macros.cpp

main.o : main.cpp Adder.hpp
	hpxcxx -g -c -I. main.cpp

libAdder.so : Adder_macros.o
	hpxcxx -g -fPIC --comp=Adder Adder_macros.o

main : libAdder.so main.o
	hpxcxx -g -fPIC --exe=main libAdder.so main.o 

clean : polish
	rm -fr main *.o *.so Adder.hpp Adder_macros.cpp

polish:
	rm -fr hpx.*.log core.*
