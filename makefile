CC = clang
CFLAGS = -Wall -std=c99 -pedantic
SWIG = swig -python
INTERFACE = molecule.i
PY_HEADER = /usr/include/python3.9
PY_LIB = /usr/lib/python3.9/config3.9m-x86_64-linux-gnu
SRC = src/
BIN = bin/

# cd /mnt/c/Users/Elman/Downloads/UofG/2750w23/molecule-webserver
# The 'FILE' environment variable can be replaced to excecute any .c file (e.g. test1)
# If a compile error states the library path cannot be found, enter the following:
# 	export LD_LIBRARY_PATH=:/mnt/c/Users/Elman/Downloads/UofG/2750w23/molecule-webserver



$(BIN)_molecule.so: $(BIN)molecule_wrap.o $(BIN)libmol.so
	$(CC) $(BIN)molecule_wrap.o -shared -L$(PY_LIB) -L$(BIN). -lmol -lm -o $(BIN)_molecule.so

$(BIN)molecule_wrap.o: molecule_wrap.c molecule.py
	$(CC) $(CFLAGS) -c -I$(PY_HEADER) molecule_wrap.c -fPIC -o $(BIN)molecule_wrap.o

$(BIN)libmol.so: $(BIN)mol.o
	$(CC) $(BIN)mol.o -shared -o $(BIN)libmol.so

$(BIN)mol.o: mol.c mol.h
	$(CC) $(CFLAGS) -c mol.c -fPIC -o $(BIN)mol.o

molecule_wrap.c: $(INTERFACE)
	$(SWIG) $(INTERFACE)

molecule.py: $(INTERFACE)
	$(SWIG) $(INTERFACE)

clean:
	rm -f *.o *.so 
	rm -f $(BIN)*.o $(BIN)*.so
	