#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

int main() {

  int fd1 = open("/tmp/myfifo", O_RDONLY);
  if (fd1 == -1) {
    perror("open fifo");
    exit(1);
  }

  char str1[80];
  while (1) {
    if (read(fd1, str1, 80) <= 0) {
      perror("read");
      exit(1);
    }

    printf("User: %s", str1);
  }
  return 0;
}
