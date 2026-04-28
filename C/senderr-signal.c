#include <errno.h>
#include <fcntl.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

int fd, work = 1;

void handle_SIGPIPE(int sig) {
  printf("Otrzymano SIGPIPE, ale program dziala dalej :)\n");
  if (close(fd) == -1) {
    perror("close fd");
    exit(1);
  }
  work = 0;
}

void handle_CTRLC(int sig) {
  printf("\nProgram zaraz sie zakonczy, sprzatam...\n");
  if (close(fd) == -1 && work == 1) {
    perror("close fd");
    exit(1);
  }
  unlink("/tmp/myfifo");
  exit(0);
}

void handle_SIGUSER(int sig) {
  printf("Wyłapano SIGUSR1, program bedzie kontynuowal prace\n");
}

int main() {
  char *myfifo = "/tmp/myfifo";
  if (mkfifo(myfifo, 0666) == -1) {
    perror("mkfifo");
    exit(1);
  }
  char arr[100];
  fd = open(myfifo, O_WRONLY);
  if (fd == -1) {
    perror("open");
    exit(1);
  }

  if (signal(SIGPIPE, handle_SIGPIPE) == SIG_ERR) {
    perror("SIGPIPE");
    exit(1);
  }

  if (signal(SIGINT, handle_CTRLC) == SIG_ERR) {
    perror("SIG_CTRL_C");
    exit(1);
  }
  if (signal(SIGUSR1, handle_SIGUSER) == SIG_ERR) {
    perror("SIGUSR");
    exit(1);
  }

  pid_t pid = getpid();

  if (kill(pid, SIGUSR1) == -1) {
    perror("kill");
    exit(1);
  }
  while (1) {
    if (fgets(arr, sizeof(arr), stdin)) {
      if (work == 1) {
        if (write(fd, arr, strlen(arr) + 1) == -1) {
          if (errno != EPIPE) {
            perror("write");
          }
        }
      }
    } else {
      perror("fgets");
      exit(1);
    }
  }
}
