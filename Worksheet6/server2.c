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

void process_client(int client_fd, unsigned long endereco,
                    unsigned short porto);
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
        process_client(client, client_addr.sin_addr.s_addr,
                       client_addr.sin_port);
        exit(0);
      }
      close(client);
    }
  }
  return 0;
}

void process_client(int client_fd, unsigned long endereco,
                    unsigned short porto) {

  char send[BUF_SIZE];

  sprintf(send, "IPv4: %lu PORTO: %hu\n", endereco, porto);

  printf("sent: %s", send);
  write(client_fd, (void *)send, sizeof(char) * BUF_SIZE);
  fflush(stdout);
  close(client_fd);
}

void erro(char *msg) {
  printf("Erro: %s\n", msg);
  exit(-1);
}
