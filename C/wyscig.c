#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/shm.h>
#include <unistd.h>

void shared_memory_actions(key_t klucz, int *shared_id, int *created,
														int **saldo) {
  *created = 1;

  *shared_id = shmget(klucz, sizeof(int), IPC_CREAT | IPC_EXCL | 0600);

  if (*shared_id == -1) {
    if (errno != EEXIST) {
      perror("shmget_creating");
      exit(1);
    }

    *created = 0;
    *shared_id = shmget(klucz, sizeof(int), 0600);
    if (*shared_id == -1) {
      perror("existing shmget");
      exit(1);
    }
  }

  *saldo = shmat(*shared_id, NULL, 0);
  if (*saldo == (void *)-1) {
    perror("shmat");
    exit(1);
  }
}

void operacja(int *saldo, int wartosc) {

  for (int i = 0; i < 5; i++) {

    int tmp = *saldo;
		printf("W tmp przed dodaniem: %d\n", tmp);
    sleep(1);
    tmp += wartosc;
		sleep(1);
		printf("W tmp po dodaniu: %d\n", tmp);
    *saldo = tmp;
    printf("Wartosc wynosi: %d\n", *saldo);
  }
}

void czyszczenie(int *saldo, int shared_id, int created) {
  if (shmdt(saldo) == -1) {
    perror("shmdt");
  }
  if (created) {
    sleep(1);
    if (shmctl(shared_id, IPC_RMID, NULL) == -1) {
      perror("shmctl_shared_id");
      exit(1);
    } else {
      printf("Pamiec wspoldzielona zostala usunięta\n");
    }
  }
}

int main(int argc, char **argv) {

  if (argc < 2) {
    fprintf(stderr, "Uzycie: %s <liczba>\n", argv[0]);
    return 1;
  }
  printf("Teraz dziala proces %d\n", getpid());

  int *saldo = NULL;
  key_t klucz = 13;
  int created;
  int shared_id;

  shared_memory_actions(klucz, &shared_id, &created, &saldo);

  if (created != 0) {

    *saldo = 0;
  }

  operacja(saldo, atoi(argv[1]));
  czyszczenie(saldo, shared_id, created);
}
