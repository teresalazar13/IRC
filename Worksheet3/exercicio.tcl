set ns [new Simulator]
set nf [open out.nam w]
$ns namtrace-all $nf

$ns color 1 Brown
$ns color 2 Orange
$ns color 3 Pink

proc fim {} {
  global ns nf
  $ns flush-trace
  close $nf
  exec nam out.nam
  exit 0;
}

set n0 [$ns node]
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]

# C = 13 Mbps e Tp = 5.24 ms  BERLIM --- PARIS
$ns duplex-link $n0 $n1 13Mb 5.24ms DropTail
# C = 40 Mbps e Tp = 6.35 ms  PARIS --- MADRID
$ns duplex-link $n1 $n2 40Mb 6.35ms DropTail
# C = 320 Mbps e Tp = 2.565 ms   MADRID --- COIMBRA
$ns duplex-link $n0 $n1 320Mb 2.565ms DropTail

# cria um agente UDP e liga-o ao nó n0
set udp0 [new Agent/UDP]
$ns attach-agent $n0 $udp0

# cria uma fonte de tráfego CBR e liga-a ao udp0
# 1 KB = 1024 B
set cbr0 [new Application/Traffic/CBR]
$cbr0 set packetSize_ 1024
$cbr0 set interval_ 1
$cbr0 set maxpkts_ 1
$cbr0 attach-agent $udp0

# cria um agente UDP e liga-o ao nó n1
set udp1 [new Agent/UDP]
$ns attach-agent $n1 $udp1

set cbr1 [new Application/Traffic/CBR]
$cbr1 set rate_ 28Mb
$cbr1 attach-agent $udp1

set udp2 [new Agent/UDP]
$ns attach-agent $n2 $udp2

set null2 [new Agent/Null]
$ns attach-agent $n2 $null2

# cria um agente Null e liga-o ao nó n3
set null3 [new Agent/Null]
$ns attach-agent $n3 $null3

$ns connect $udp0 $null3
$ns connect $udp1 $null2

$ns at 0.1 "$cbr0 start"
$ns at 0.1 "$cbr1 start"
$ns at 4.0 "$cbr0 stop"
$ns at 4.0 "$cbr1 stop"

$udp0 set class_ 1
$udp1 set class_ 2
$udp2 set class_ 3

$ns at 5.0 "fim"

$ns run
