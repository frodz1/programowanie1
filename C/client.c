#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/select.h>
#include <sys/socket.h>
#include <unistd.h>

int main() {
  int sock;
  struct sockaddr_in serv;
  char buf[1024];

  sock = socket(AF_INET, SOCK_STREAM, 0);
  if (sock < 0) { perror("socket"); exit(1); }

  serv.sin_family = AF_INET;
  serv.sin_port = htons(8080);
  inet_pton(AF_INET, "127.0.0.1", &serv.sin_addr);

  if (connect(sock, (struct sockaddr*)&serv, sizeof(serv)) < 0) {
    perror("connect");
    exit(1);
  }

  printf("Połączono z serwerem.\n");

  while (1) {
    fd_set rfds;
    FD_ZERO(&rfds);
    FD_SET(sock, &rfds);
    FD_SET(STDIN_FILENO, &rfds);

    int maxfd = sock > STDIN_FILENO ? sock : STDIN_FILENO;

    if (select(maxfd + 1, &rfds, NULL, NULL, NULL) < 0) {
      perror("select");
      break;
    }

    if (FD_ISSET(sock, &rfds)) {
      ssize_t n = read(sock, buf, sizeof(buf) - 1);
      if (n <= 0) {
        printf("Serwer rozłączył.\n");
        break;
      }
      buf[n] = 0;
      printf("%s", buf);
    }

    if (FD_ISSET(STDIN_FILENO, &rfds)) {
      if (!fgets(buf, sizeof(buf), stdin)) {
        printf("Koniec stdin.\n");
        shutdown(sock, SHUT_WR);
        break;
      }
      send(sock, buf, strlen(buf), 0);
    }
  }

  close(sock);
  return 0;
}

