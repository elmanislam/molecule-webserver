CC = clang
CFLAGS = -Wall -std=c99 -pedantic
SWIG = swig -python
INTERFACE = molecule.i
PY_HEADER = /usr/include/python3.9
PY_LIB = /usr/lib/python3.9/config3.9m-x86_64-linux-gnu
SRC = src/
BIN = bin/
LIB = lib/
BACK = back-end/

# cd /mnt/c/Users/Elman/Downloads/UofG/2750w23/molecule-webserver
# The 'FILE' environment variable can be replaced to excecute any .c file (e.g. test1)
# If a compile error states the library path cannot be found, enter the following:
# 	export LD_LIBRARY_PATH=:/mnt/c/Users/Elman/Downloads/UofG/2750w23/molecule-webserver/lib



$(LIB)_molecule.so: $(BIN)molecule_wrap.o $(LIB)libmol.so
	$(CC) $(BIN)molecule_wrap.o -shared -L$(PY_LIB) -L$(LIB). -lmol -lm -o $(LIB)_molecule.so

$(BIN)molecule_wrap.o: $(BACK)molecule_wrap.c $(BACK)molecule.py
	$(CC) $(CFLAGS) -c -I$(PY_HEADER) $(BACK)molecule_wrap.c -fPIC -o $(BIN)molecule_wrap.o

$(LIB)libmol.so: $(BIN)mol.o
	$(CC) $(BIN)mol.o -shared -o $(LIB)libmol.so

$(BIN)mol.o: $(BACK)mol.c $(BACK)mol.h
	$(CC) $(CFLAGS) -c $(BACK)mol.c -fPIC -o $(BIN)mol.o

$(BACK)molecule_wrap.c: $(BACK)$(INTERFACE)
	$(SWIG) $(BACK)$(INTERFACE)

$(BACK)molecule.py: $(BACK)$(INTERFACE)
	$(SWIG) $(BACK)$(INTERFACE)

clean:
	rm -f *.o *.so 
	rm -f $(BIN)*.o $(BIN)*.so
	rm -f $(LIB)*.o $(LIB)*.so