#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <unistd.h>
#include <netdb.h>
#define BUFLEN 512	// Tamanho do buffer
#define PORT 9876	// Porto para recepção das mensagens

void erro(char *s) {
	perror(s);
	exit(1);
}

int main(int argc, char *argv[]) {
	struct sockaddr_in si_minha, si_outra;
	char endServer[100];
	int s,recv_len;
	struct hostent *hostPtr;
	socklen_t slen = sizeof(si_outra);
	char buf[BUFLEN];

	strcpy(buf,argv[3]);

  strcpy(endServer, argv[1]);
  if ((hostPtr = gethostbyname(endServer)) == 0)
	  erro("Nao consegui obter endereço");


	// Cria um socket para recepção de pacotes UDP
	if((s=socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) == -1)
		erro("Erro na criação do socket");

	si_minha.sin_family = AF_INET;
	si_minha.sin_port = htons(PORT);
	si_minha.sin_addr.s_addr = ((struct in_addr *)(hostPtr->h_addr))->s_addr;

	// Envio de mensagem
	if(sendto(s, buf, BUFLEN, 0, (struct sockaddr *) &si_minha,slen) == -1)
		erro("Erro no sendto");

	printf("Mensagem enviada: %s\n" , buf);

  if((recv_len = recvfrom(s, buf, BUFLEN, 0, (struct sockaddr *) &si_minha, &slen)) == -1)
    erro("Erro no recvfrom");

  printf("Mensagem traduzida: %s\n" , buf);

	// Fecha socket e termina programa
	close(s);
	return 0;
}

// ./client2 127.0.0.1 9876 "Thanks"
