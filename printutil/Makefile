HPX_LIB_DIR=/usr/local/lib64

run: main
	LD_LIBRARY_PATH=.:$(HPX_LIB_DIR) ./main 

PrintUtil.hpp PrintUtil_macros.cpp : PrintUtil.py
	python3 PrintUtil.py

PrintUtil.o : PrintUtil.cpp PrintUtil.hpp
	hpxcxx -fPIC -g -c -I. PrintUtil.cpp

PrintUtil_macros.o : PrintUtil_macros.cpp PrintUtil.hpp
	hpxcxx -fPIC -g -c -I. PrintUtil_macros.cpp

main.o : main.cpp PrintUtil.hpp
	hpxcxx -g -c -I. main.cpp

libPrintUtil.so : PrintUtil.o PrintUtil_macros.o
	hpxcxx -g -fPIC --comp=PrintUtil PrintUtil.o PrintUtil_macros.o

main : libPrintUtil.so main.o
	hpxcxx -g -fPIC --exe=main libPrintUtil.so main.o PrintUtil.o

clean : polish
	rm -fr main *.o *.so

polish:
	rm -fr hpx.*.log core.*
