#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>
#include <errno.h>

int main(){
	char *recfifo = malloc(512);
	if (recfifo == NULL) {
		perror("malloc recfifo");
		return 1;
	}
	
	char pathname[512];
	char *brfifo = "/tmp/broker_msg";
	char msg[512];

	sprintf(recfifo, "/tmp/%d", getpid());
	printf("FIFO MA SCIEZKE: %s\n", recfifo); 
	sprintf(pathname, "REC: %s",recfifo);
	if (mkfifo(recfifo, 0666) == -1) {
		if (errno != EEXIST) {
			perror("mkfifo recifo");
			return 1;
	}
	}
	
	int sciezka = open(brfifo, O_WRONLY);
	if (sciezka == -1) {
		perror("open brfifo");
		return 1;
	}

 	if (write(sciezka, pathname,strlen(pathname)) == -1) {
		perror("write do brokera");
		return 1;
	}	

	int message = open(recfifo, O_RDONLY); 
	if (message == -1) { 
		perror("open recfifo");
		return 1;
	}
	ssize_t n;
	while ((n=read(message, msg, sizeof(msg)-1)) >0) { 
	msg[n] = '\0';
	printf("%s\n", msg); 
	
	}
	perror("read recfifo");
	


}
