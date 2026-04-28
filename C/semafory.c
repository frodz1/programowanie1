#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/sem.h>
#include <sys/shm.h>
#include <unistd.h>

void sem_lock(int semid) {
  struct sembuf op = {0, -1, 0};
  if (semop(semid, &op, 1) == -1) {
    perror("semop lock");
    exit(1);
  }
}

void sem_unlock(int semid) {
  struct sembuf op = {0, +1, 0};
  if (semop(semid, &op, 1) == -1) {
    perror("semop unlock");
    exit(1);
  }
}

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

int sem_actions(key_t sem_key, int *created) {
  int semid = semget(sem_key, 1, IPC_CREAT | 0600);
  if (semid == -1) {
    perror("semget");
    exit(1);
  }

  if (*created) {
    if (semctl(semid, 0, SETVAL, 1) == -1) {
      perror("semctl SETVAL");
      exit(1);
    }
  }

  return semid;
}

void operacja(int *saldo, int wartosc, int semid) {

  for (int i = 0; i < 5; i++) {
    sem_lock(semid);

    int tmp = *saldo;
    usleep(100);
    tmp += wartosc;
    *saldo = tmp;

    printf("Wartosc wynosi: %d\n", *saldo);

    sem_unlock(semid);
  }
}

void czyszczenie(int *saldo, int shared_id, int created, int semid) {
  if (shmdt(saldo) == -1) {
    perror("shmdt");
  }
  if (created != 0) {
    sleep(5);
    if (shmctl(shared_id, IPC_RMID, NULL) == -1) {
      perror("shmctl_shared_id");
      exit(1);
    } else {

      printf("Pamiec wspoldzielona zostala usunięta\n");
    }

    if (semctl(semid, 0, IPC_RMID) == -1) {
      perror("semctl IPC_RMID");
    } else {
      printf("Semafor usuniety\n");
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
  int sem_klucz = 17;
  int created;
  int shared_id;
  int semid;

  shared_memory_actions(klucz, &shared_id, &created, &saldo);
  semid = sem_actions(sem_klucz, &created);
  if (created != 0) {

    *saldo = 0;
  }

  operacja(saldo, atoi(argv[1]), semid);
  czyszczenie(saldo, shared_id, created, semid);
}
