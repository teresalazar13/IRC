set ns [new Simulator]
# criar um novo objecto simulador. e um container da simulaçao. dentro de [] criar um simulador e devolve a referencia. set -> atribuiçao var

set nf [open out.nam w]
# abre o ficheiro out.nam para escrita
$ns namtrace-all $nf
# utiliza a var ns que tem ref para o simulador gerar um ficheiro de trace. tem como parametro o ficheiro para o qual queremos enviar o resultado

proc fim {} {
  global ns nf
  # vai usar as variaveis globais
  $ns flush-trace
  # metodo que pega em todos os dados da simulaçao e vai envia-los para o ficheiro
  close $nf
  exec nam out.nam
  # executa como aplicaçao externa o ficheiro out.nam
  exit 0;
}

set n0 [$ns node]
# um objecto nó é criado através do comando $ns node
set n1 [$ns node]
$ns duplex-link $n0 $n1 1Mb 10ms DropTail
# define uma ligação duplex (para os dois lados) entre os dois nós n0 e n1 com a largura de banda de 1 Mbps, com um atraso de 10ms e com uma fila do tipo DropTail(fila a que esta associada a ligaçao)

set udp0 [new Agent/UDP]
# cria um agente UDP e liga-o ao nó n0
$ns attach-agent $n0 $udp0

set cbr0 [new Application/Traffic/CBR]
# cria uma fonte de tráfego CBR e liga-a ao udp0
$cbr0 set packetSize_ 500
# tamanho do pacote de 500 bytes
$cbr0 set interval_ 0.005
# intervalo do pacote - 200 pacotes por segundo (1 em cada 0.005 segundos)
$cbr0 attach-agent $udp0
# ligador o cbr0 a udp0

set null0 [new Agent/Null]
# sitio onde os pacotes estao a chegar. mas eles chegam, deitam-nos fora (NULL)
$ns attach-agent $n1 $null0
# cria um agente Null e liga-o ao nó n1

$ns connect $udp0 $null0
# depois de definidos os dois agentes, é necessário proceder à sua ligação. é necessario porque podem estar a haver muitas ligaçoes ao mesmo tempo.

$ns at 0.5 "$cbr0 start"
$ns at 4.5 "$cbr0 stop"

$ns at 5.0 "fim"
# evoca o procedimento fim após 5.0 segundos de tempo de simulação.

$ns run
# para a simulaçao iniciar
