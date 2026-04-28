#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <errno.h>

int main() {
	char msg[100];
	char *fifo = "/tmp/broker_msg";
	if (mkfifo(fifo, 0666) == -1) {
		if (errno != EEXIST) {
			perror("mkfifo broker_msg");
			return 1;
		}
	}

	int wiadomosci = open(fifo, O_RDONLY);
	if (wiadomosci == -1) {
        	perror("open broker_msg");
        	return 1;
    }

	int do_receivera[10];
	
	int ile_receiverow = 0;


while(1){

	ssize_t n = read(wiadomosci, msg, sizeof(msg)-1);
	if (n== -1) {
		perror("read broker_msg");
		continue;
	}
	msg[n] = '\0';
	char *real_msg = msg + 5;


	if (msg[0] == 'M' && msg[1] == 'S' && msg[2] == 'G'){
	
		for (int i = 0; i < ile_receiverow; i++) {
		if (write(do_receivera[i], real_msg, strlen(real_msg)) == -1) {
			perror("write do receivera");
	}
	}
	}
	if(msg[0] == 'R' && msg[1] == 'E' && msg[2] == 'C') {
			if (ile_receiverow < 9) {
				do_receivera[ile_receiverow] = open(real_msg, O_WRONLY);
			
				if (do_receivera[ile_receiverow] == -1) {
                			perror("open do_receivera");
                			return 1;
				}

				printf("Otworzono fifo do receivera\n");
				ile_receiverow +=1;
			} else{
				printf("Osiągnięto limit receiverow\n");
			}
	}

		
}
}
