CC = g++
all: scarebot.exe
scarebot.exe: scarebot.o
	$(CC) scarebot.o -o scarebot.exe -lsfml-graphics -lsfml-window -lsfml-system -lsfml-audio
scarebot.o: scarebot.cpp
	$(CC) -c scarebot.cpp

clean:
	rm *.o
	rm *.exe