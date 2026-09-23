CC=gcc
CFLAGS=-Wall
MAKE=make

all: driver

driver: driver.o thread.o list.o debug.o schedule.o
	$(CC) $(CFLAGS) -o $@ driver.o thread.o list.o debug.o schedule.o

driver.o: driver.c thread.h schedule.h
	$(CC) $(CFLAGS) -c $< -o $@

thread.o: thread.c thread.h
	$(CC) $(CFLAGS) -c $< -o $@

list.o: list.c list.h
	$(CC) $(CFLAGS) -c $< -o $@

debug.o: debug.c debug.h
	$(CC) $(CFLAGS) -c $< -o $@

schedule.o: schedule.c schedule.h thread.h list.h
	$(CC) $(CFLAGS) -c $< -o $@

.PHONY clean:
	@rm *.o driver
