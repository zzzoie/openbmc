lib: libshim.so

libshim.so: shim_lib.c
	$(CC) $(CFLAGS) -fPIC -c -o shim_lib.o shim_lib.c
	$(CC) -shared -o libshim.so shim_lib.o -lc $(LDFLAGS)

.PHONY: clean

clean:
	rm -rf *.o libshim.so
