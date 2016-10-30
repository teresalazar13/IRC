set ns [new Simulator]
set nf [open out.nam w]
$ns namtrace-all $nf

$ns color 1 Blue
$ns color 2 Red
$ns color 3 Black

proc fim {} {
	global ns nf
	$ns flush-trace
	close $nf
	exec nam out.nam
	exit 0
}

set n0 [$ns node]
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]

#C = 0.02 Mb e Tp = 1.45ms
$ns duplex-link $n0 $n1 0.02Mb 1.45ms DropTail
#C = 2 Mb e Tp de 8ms
$ns duplex-link $n2 $n3 2Mb 8ms DropTail
#C = 20 Mb e Tp de 67ms
$ns duplex-link $n4 $n5 20Mb 67ms DropTail

set udp0 [new Agent/UDP]
$ns attach-agent $n0 $udp0

#1 KB = 1024 bytes
set cbr0 [new Application/Traffic/CBR]
$cbr0 set packetsize_ 1024
$cbr0 set interval_ 1
$cbr0 set maxpkts_ 1
$cbr0 attach-agent $udp0

set udp2 [new Agent/UDP]
$ns attach-agent $n2 $udp2

#1 KB = 1024 bytes
set cbr2 [new Application/Traffic/CBR]
$cbr2 set packetsize_ 1024
$cbr2 set interval_ 1
$cbr2 set maxpkts_ 1
$cbr2 attach-agent $udp2

set udp4 [new Agent/UDP]
$ns attach-agent $n4 $udp4

#1 KB = 1024 bytes
set cbr4 [new Application/Traffic/CBR]
$cbr4 set packetsize_ 1024
$cbr4 set interval_ 1
$cbr4 set maxpkts_ 1
$cbr4 attach-agent $udp4

set null0 [new Agent/Null]
$ns attach-agent $n1 $null0

set null2 [new Agent/Null]
$ns attach-agent $n3 $null2

set null4 [new Agent/Null]
$ns attach-agent $n5 $null4

$ns connect $udp0 $null0
$ns connect $udp2 $null2
$ns connect $udp4 $null4

$ns at 0.1 "$cbr0 start"
$ns at 0.1 "$cbr2 start"
$ns at 0.1 "$cbr4 start"
$ns at 4.0 "$cbr0 stop"
$ns at 4.0 "$cbr2 stop"
$ns at 4.0 "$cbr4 stop"

$udp0 set class_ 1
$udp2 set class_ 2
$udp4 set class_ 3

$ns at 5.0 "fim"

$ns run
