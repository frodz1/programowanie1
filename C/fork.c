#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <string.h>

int main(int argc, char* argv[]){

	if (argc != 2) {
	       printf ("Zła ilość argumentów\n");
       		exit(1);
	}		

        char buf[256];
        int p[2];

        if(pipe(p) < 0){
		perror("pipe");
                exit(1);
	}

        pid_t pid = fork();

        if (pid < 0) {
                perror ("Blad fork");
                exit(1);
        }

        if (pid > 0) {
		if (close(p[1]) != 0){
			perror("close");
			exit(1);
		}
                ssize_t n;
        	size_t total_read = 0;
                while ((n = read(p[0], buf, sizeof(buf)-1)) > 0) {
            buf[n] = '\0';
            printf("%s", buf);
	    total_read += (size_t)n;
                }
		wait(NULL);
		printf("Przesłano %zu bajtow.\n", total_read);
		 if (close(p[0]) != 0){
                        perror("close rodzica");
                	exit(1);
		 }
        }else {
		if (close(p[0]) != 0){
                	perror("close");
			exit(1);
                }

        if (dup2(p[1], STDOUT_FILENO) < 0) {
        perror("dup2");
        exit(1);
        }
	 if (close(p[1]) != 0){
         	perror("close");
      		exit(1);	        
       	 }
        execlp(argv[1], argv[1], (char*)NULL);

        perror("exec");
        exit(1);
        }
    return 0;
}
