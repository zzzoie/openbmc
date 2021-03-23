lib: libshim-list.so

C_SRCS := $(SOURCES)
C_OBJS := ${C_SRCS:.c=.o}

libshim-list.so: $(C_OBJS)
	$(CC) -shared -o libshim-list.so $^ -fPIC -lc -Wl,--whole-archive -lm -Wl,--no-whole-archive -lrt $(LDFLAGS)

$(C_SRCS:.c=.d):%.d:%.c
	$(CC) $(CFLAGS) $< >$@

.PHONY: clean

clean:
	rm -rf *.o libshim-list.so
