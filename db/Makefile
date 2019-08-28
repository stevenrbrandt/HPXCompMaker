HPX_LIB_DIR=/usr/local/lib64

run: main db.so
	LD_LIBRARY_PATH=.:$(HPX_LIB_DIR) ./main 
	LD_LIBRARY_PATH=.:$(HPX_LIB_DIR) python3 db_test.py

#init_globally.o : init_globally.cpp
#	hpxcxx -fPIC -g -c init_globally.cpp

db.so : db_py11.o libDb.so #init_globally.o
	g++ -g -fPIC -shared -o db.so db_py11.o libDb.so #init_globally.o

db_py11.o : db_py11.cpp Db.hpp
	hpxcxx -g -fPIC -c -I/usr/include/python3.6m -I. db_py11.cpp

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
