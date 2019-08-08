HPX_LIB_DIR=/usr/local/lib64

run: main
	LD_LIBRARY_PATH=.:$(HPX_LIB_DIR) ./main 

Db.hpp Db_macros.cpp : Db.py
	python3 Db.py

Db_macros.o : Db_macros.cpp Db.hpp
	hpxcxx -fPIC -g -c -I. Db_macros.cpp

main.o : main.cpp Db.hpp
	hpxcxx -g -c -I. main.cpp

libDb.so : Db_macros.o
	hpxcxx -g -fPIC --comp=Db Db_macros.o

main : libDb.so main.o
	hpxcxx -g -fPIC --exe=main libDb.so main.o 

clean : polish
	rm -fr main *.o *.so Db.hpp Db_macros.cpp

polish:
	rm -fr hpx.*.log core.*
