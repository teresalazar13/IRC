#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
  char msg[50];
  char buffer[50];
  char msg_check[50];
  char buffer_check[50];
  int fileids[2];
  int fileids_check[2];
  if (pipe(fileids) == 0 && pipe(fileids_check) == 0) { // Criou o pipe, sem erros
    pid_t mypid = getpid();
    if (fork() == 0) { // Processo Filho
      close(fileids[0]); // Fecha o descritor de leitura
      sprintf(msg, "Olá pai, o meu pid é %d!", getpid());
      write (fileids[1], msg, sizeof(msg));
      close(fileids[1]); // Fecha o descritor de escrita
      close(fileids_check[1]); // Fecha o descritor de escrita
      read(fileids_check[0], buffer_check, sizeof(buffer_check));
      // printf("%d %d\n", atoi(buffer_check), getppid() );
      if (getppid() != atoi(buffer_check)) {
        printf("Error\n");
      }
      close(fileids_check[0]); // Fecha o descritor de leitura
    }
    else { // Processo Pai
      close(fileids[1]); // Fecha o descritor de escrita
      read(fileids[0], buffer, sizeof(buffer));
      printf("%s\n", buffer);
      close(fileids[0]); // Fecha o descritor de leitura
      close(fileids_check[0]); // Fecha o descritor de leitura
      sprintf(msg_check, "%d", mypid);
      write (fileids_check[1], msg_check, sizeof(msg_check));
      close(fileids_check[1]); // Fecha o descritor de escrita
    }
  }
  else {
    printf("ERRO na criação do PIPE!\n");
  }
  exit(0);
}
