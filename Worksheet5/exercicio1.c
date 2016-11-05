#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

int main(int argc, char const *argv[]) {
  pid_t mypid;
  pid_t childpid;
  mypid = getpid();
  childpid = fork();
  if (childpid == 0) {
    printf("Eu sou o processo filho, o meu pid é %d e o do meu pai é %d\n", getpid(), mypid );
  }
  else {
    printf("Eu sou o processo pai, o meu pid é %d e o do meu filho é %d\n", mypid, childpid);
  }
  return 0;
}
