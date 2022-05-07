spreader.out : spreader.o spreaderRunner.o  
	g++ -ansi -Wall -v -pg -no-pie -fno-builtin -o spreader.out spreader.o spreaderRunner.o 

spreader.o : spreader.cpp spreader.h 
	g++ -ansi -Wall -v -pg -no-pie -fno-builtin -c spreader.cpp

spreaderRunner.o : spreaderRunner.cpp CPUTimer.h spreaderRunner.h spreader.h 
	g++ -ansi -Wall -v -pg -no-pie -fno-builtin -c spreaderRunner.cpp

clean : 
	rm -f spreader.out spreader.o  spreaderRunner.o   
