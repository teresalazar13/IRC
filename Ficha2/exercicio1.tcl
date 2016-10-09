set ns [new Simulator]
set nf [open out.nam w]
$ns namtrace-all $nf

$ns color 1 Blue
$ns color 2 Red

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

# C = 7 Mbps e Tp = 1,5 ms
$ns duplex-link $n0 $n1 7Mb 1.5ms DropTail
# C = 480 Mbps e Tp = 0.67 ms
$ns duplex-link $n2 $n3 480Mb 0.67ms DropTail

# cria um agente UDP e liga-o ao nó n0
set udp0 [new Agent/UDP]
$ns attach-agent $n0 $udp0

# cria uma fonte de tráfego CBR e liga-a ao udp0
# 100 KB = 102400 bytes
set cbr0 [new Application/Traffic/CBR]
$cbr0 set packetSize_ 102400
$cbr0 set interval_ 1
$cbr0 set maxpkts_ 1
$cbr0 attach-agent $udp0

# cria um agente UDP e liga-o ao nó n2
set udp2 [new Agent/UDP]
$ns attach-agent $n2 $udp2

# cria uma fonte de tráfego CBR e liga-a ao udp2
# 100 KB = 102400 bytes
set cbr2 [new Application/Traffic/CBR]
$cbr2 set packetSize_ 102400
$cbr2 set interval_ 1
$cbr2 set maxpkts_ 1
$cbr2 attach-agent $udp2

# cria um agente Null e liga-o ao nó n1
set null0 [new Agent/Null]
$ns attach-agent $n1 $null0

# cria um agente Null e liga-o ao nó n3
set null2 [new Agent/Null]
$ns attach-agent $n3 $null2

$ns connect $udp0 $null0
$ns connect $udp2 $null2

$ns at 0.1 "$cbr0 start"
$ns at 0.1 "$cbr2 start"
$ns at 4.0 "$cbr0 stop"
$ns at 4.0 "$cbr2 stop"

$udp0 set class_ 1
$udp2 set class_ 2

$ns at 5.0 "fim"

$ns run
