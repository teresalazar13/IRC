/*******************************************************************
* SERVIDOR no porto 9000, à escuta de novos clientes. Quando surjem
* novos clientes os dados por eles enviados são lidos e descarregados no ecra
*******************************************************************/

#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

#define SERVER_PORT 9000
#define BUF_SIZE 1024

void process_client(int fd);
void erro(char *msg);

int main() {
  int fd, client;
  struct sockaddr_in addr, client_addr;
  int client_addr_size;

  bzero((void *)&addr, sizeof(addr));
  addr.sin_family = AF_INET; // Domínio no qual o socket será usado
  addr.sin_addr.s_addr = htonl(INADDR_ANY); // Qualquer endereço do host
  addr.sin_port = htons(SERVER_PORT);       // Porto a associar

  if ((fd = socket(AF_INET, SOCK_STREAM, 0)) < 0) // Cria um novo socket
    erro("na funcao socket");
  if (bind(fd, (struct sockaddr *)&addr, sizeof(addr)) <
      0) // Associa um socket a um determinado endereço
    erro("na funcao bind");
  if (listen(fd, 5) < 0) // Aguarda pela recepção de ligações
    erro("na funcao listen");

  while (1) {
    client_addr_size = sizeof(client_addr);
    client = accept(fd, (struct sockaddr *)&client_addr,
                    (socklen_t *)&client_addr_size); // Aceita uma ligação
    if (client > 0) {
      if (fork() == 0) {
        close(fd);
        process_client(client);
        exit(0);
      }
      close(client);
    }
  }
  return 0;
}

void process_client(int client_fd) {
  int nread = 0;
  char buffer[BUF_SIZE];
  char temp[BUF_SIZE];
  char invertedBuffer[BUF_SIZE];
  nread = read(client_fd, buffer, BUF_SIZE - 1);
  buffer[nread] = '\0';
  int i;

  for (i = 0; i < strlen(buffer); i++) {
    invertedBuffer[strlen(buffer) - i - 1] = buffer[i];
  }

  invertedBuffer[i] = '\0';

  write(client_fd, invertedBuffer, sizeof(invertedBuffer));
  printf("sent: %s\n", invertedBuffer);
  fflush(stdout);
  close(client_fd);
}

void erro(char *msg) {
  printf("Erro: %s\n", msg);
  exit(-1);
}
