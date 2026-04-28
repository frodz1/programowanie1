#include <arpa/inet.h>
#include <errno.h>
#include <netinet/in.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/select.h>
#include <sys/socket.h>
#include <unistd.h>

static int clients[128];
static int n_clients = 0;

static void remove_client(int idx) {
  int fd = clients[idx];
  close(fd);

  clients[idx] = clients[n_clients - 1];
  n_clients--;
}

static void broadcast_msg(const char *msg, size_t len) {
  for (int i = 0; i < n_clients;) {
    if (send(clients[i], msg, len, 0) < 0) {
      perror("send");
      remove_client(i);
    } else {
      i++;
    }
  }
}

int main() {
  signal(SIGPIPE, SIG_IGN);

  int server_fd = socket(AF_INET, SOCK_STREAM, 0);
  if (server_fd < 0) {
    perror("socket");
    return 1;
  }

  int opt = 1;
  setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

  struct sockaddr_in addr;
  memset(&addr, 0, sizeof(addr));
  addr.sin_family = AF_INET;
  addr.sin_addr.s_addr = INADDR_ANY;
  addr.sin_port = htons(8080);

  if (bind(server_fd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
    perror("bind");
    return 1;
  }
  if (listen(server_fd, 16) < 0) {
    perror("listen");
    return 1;
  }

  printf("Serwer działa na porcie %d.\n", 8080);

  while (1) {
    fd_set rfds;
    FD_ZERO(&rfds);
    FD_SET(server_fd, &rfds);

    int maxfd = server_fd;

    for (int i = 0; i < n_clients; i++) {
      FD_SET(clients[i], &rfds);
      if (clients[i] > maxfd)
        maxfd = clients[i];
    }

    int r = select(maxfd + 1, &rfds, NULL, NULL, NULL);
    if (r < 0) {
      if (errno == EINTR)
        continue;
      perror("select");
      break;
    }

    if (FD_ISSET(server_fd, &rfds)) {
      socklen_t alen = sizeof(addr);
      int fd = accept(server_fd, (struct sockaddr *)&addr, &alen);
      if (fd < 0)
        perror("accept");
      else if (n_clients >= 128) {
        printf("Za dużo klientów, odrzucam fd=%d\n", fd);
        close(fd);
      } else {
        clients[n_clients++] = fd;
        printf("Nowy klient nr %d (fd=%d)\n", n_clients, fd);
      }
    }

    for (int i = 0; i < n_clients;) {
      int fd = clients[i];
      if (!FD_ISSET(fd, &rfds)) {
        i++;
        continue;
      }

      char buf[1024];
      ssize_t n = read(fd, buf, sizeof(buf) - 1);
      if (n <= 0) {
        printf("Klient nr %d rozłączony (fd=%d)\n", i + 1, fd);
        remove_client(i);
      } else {
        buf[n] = 0;
        i++;
        size_t len = sizeof(buf);
        broadcast_msg(buf, len);
      }
    }
  }

  close(server_fd);
  return 0;
}
