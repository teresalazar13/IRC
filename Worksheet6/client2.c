/*************************************************************
* CLIENTE liga ao servidor (definido em argv[1]) no porto especificado
* (em argv[2]), escrevendo a palavra predefinida (em argv[3]).
* USO: >cliente <enderecoServidor> <porto> <Palavra>
*************************************************************/

#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

void erro(char *msg);

int main(int argc, char *argv[]) {
  char endServer[100];
  int fd;
  struct sockaddr_in addr;
  struct hostent *hostPtr;

  if (argc != 3) {
    printf("cliente <host> <port>\n");
    exit(-1);
  }
  strcpy(endServer, argv[1]);

  if ((hostPtr = gethostbyname(endServer)) == 0) // Converte nome para endereço
    erro("Nao consegui obter endereço");

  bzero((void *)&addr, sizeof(addr));
  addr.sin_family = AF_INET;
  addr.sin_addr.s_addr = ((struct in_addr *)(hostPtr->h_addr))->s_addr;
  addr.sin_port = htons((short)atoi(argv[2]));

  if ((fd = socket(AF_INET, SOCK_STREAM, 0)) == -1) // Cria um novo socket
    erro("socket");
  if (connect(fd, (struct sockaddr *)&addr, sizeof(addr)) <
      0) // Inicia uma ligação num socket
    erro("Connect");

  int nread = 0;
  char buffer[1024];

  nread = read(fd, buffer, 1024 - 1);
  buffer[nread] = '\0';

  printf("recieved: %s", buffer);

  close(fd);
  exit(0);
}

void erro(char *msg) {
  printf("Erro: %s\n", msg);
  exit(-1);
}
