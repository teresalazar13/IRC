set ns [new Simulator]

$ns color 1 Pink

set nf [open out.nam w]
$ns namtrace-all $nf

proc fim {} {
  global ns nf
  $ns flush-trace
  close $nf
  exec nam out.nam
  exit 0;
}

set n0 [$ns node]
set n1 [$ns node]

# C = 3.2 Mbps e Tp = 239ms
$ns duplex-link $n0 $n1 3.2Mb 239ms DropTail

set udp0 [new Agent/UDP]
$ns attach-agent $n0 $udp0

# cria uma fonte de tráfego CBR e liga-a ao udp0
# 1 MB = 1048576 B
set cbr0 [new Application/Traffic/CBR]
$cbr0 set packetSize_ 1048576
$cbr0 set interval_ 1
$cbr0 set maxpkts_ 1
$cbr0 attach-agent $udp0

# cria um agente Null e liga-o ao nó n1
set null0 [new Agent/Null]
$ns attach-agent $n1 $null0

$ns connect $udp0 $null0

$ns at 0.1 "$cbr0 start"
$ns at 4.0 "$cbr0 stop"

$udp0 set class_ 1

$ns at 5.0 "fim"

$ns run
