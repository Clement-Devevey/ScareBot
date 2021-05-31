CC = g++
all: scarebot.exe
	chmod 777 scarebot.exe 
scarebot.exe: scarebot.o Collision.o
	$(CC) scarebot.o Collision.o -o scarebot.exe -lsfml-graphics -lsfml-window -lsfml-system -lsfml-audio
scarebot.o: scarebot.cpp
	$(CC) -c scarebot.cpp
Collision.o: Collision.cpp
	$(CC) -c Collision.cpp

clean:
	rm *.o
	rm *.exe