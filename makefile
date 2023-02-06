CC = clang
CFLAGS = -Wall -std=c99 -pedantic
FILE = main

# The 'FILE' environment variable can be replaced to excecute any .c file (e.g. test1)
# If a compile error states the library path cannot be found, enter the following:
# 	export LD_LIBRARY_PATH=:/mnt/c/Users/Elman/Downloads/2750w23/A1

all: mol

mol: $(FILE).o libmol.so
	$(CC) $(FILE).o -L. -lmol -lm -o mol

libmol.so: mol.o
	$(CC) mol.o -shared -o libmol.so

mol.o: mol.c mol.h
	$(CC) $(CFLAGS) -c mol.c -fPIC -o mol.o

$(FILE).o: $(FILE).c mol.h
	$(CC) $(CFLAGS) -c $(FILE).c -o $(FILE).o


clean:
	rm -f *.o *.so molmake 