CC = clang
CFLAGS = -Wall -std=c99 -pedantic
SWIG = swig -python
INTERFACE = molecule.i
PY_HEADER = /usr/include/python3.7
PY_LIB = /usr/lib/python3.7/config3.7m-x86_64-linux-gnu
# cd /mnt/c/Users/Elman/Downloads/UofG/2750w23/A3
# The 'FILE' environment variable can be replaced to excecute any .c file (e.g. test1)
# If a compile error states the library path cannot be found, enter the following:
# 	export LD_LIBRARY_PATH=:/mnt/c/Users/Elman/Downloads/UofG/2750w23/A3



_molecule.so: molecule_wrap.o libmol.so
	$(CC) molecule_wrap.o -shared -L$(PY_LIB) -L. -dynamiclib -lmol -lm -o _molecule.so

molecule_wrap.o: molecule_wrap.c molecule.py
	$(CC) $(CFLAGS) -c -I$(PY_HEADER) molecule_wrap.c -fPIC  -o molecule_wrap.o

libmol.so: mol.o
	$(CC) mol.o -shared -o libmol.so

mol.o: mol.c mol.h
	$(CC) $(CFLAGS) -c mol.c -fPIC -o mol.o

molecule_wrap.c: $(INTERFACE)
	$(SWIG) $(INTERFACE)

molecule.py: $(INTERFACE)
	$(SWIG) $(INTERFACE)

clean:
	rm -f *.o *.so 