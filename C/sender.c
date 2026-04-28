#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>


int main() {
	int wiadomosci;
        char msg[1024];
      	char str1[512];	
                
        char *fifo = "/tmp/broker_msg";

	wiadomosci = open(fifo, O_WRONLY);
	if (wiadomosci == -1) {
        	perror("open broker_msg");
        	return 1;
    }

	while(1) {

	
	fgets(str1, sizeof(str1), stdin);
	sprintf(msg, "MSG: %s", str1);
        if(write(wiadomosci, msg, strlen(msg)) < 0){
		perror ("write to broker_msg");
		return 1;
	}
	}
}
