set ns [new Simulator]
set nf [open out.nam w]
$ns namtrace-all $nf

$ns color 1 Pink
$ns color 2 Orange

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

# C = 6000Mbps e Tp = 2ms
$ns duplex-link $n0 $n1 6000Mb 2ms DropTail
# C = 12Mbps e Tp = 0.67ms
$ns duplex-link $n2 $n3 12Mb 0.67ms DropTail

set udp0 [new Agent/UDP]
$ns attach-agent $n0 $udp0

#20 MB = 20480 B
set cbr0 [new Application/Traffic/CBR]
$cbr0 set packetsize_ 20480
$cbr0 set interval_ 1
$cbr0 set maxpkts_ 1
$cbr0 attach-agent $udp0

set udp2 [new Agent/UDP]
$ns attach-agent $n2 $udp2

#20 MB = 20480 B
set cbr2 [new Application/Traffic/CBR]
$cbr2 set packetsize_ 20480
$cbr2 set interval_ 1
$cbr2 set maxpkts_ 1
$cbr2 attach-agent $udp2

set null0 [new Agent/Null]
$ns attach-agent $n1 $null0

set null2 [new Agent/Null]
$ns attach-agent $n3 $null2

$ns connect $udp0 $null0
$ns connect $udp2 $null2

$ns at 0.1 "$cbr0 start"
$ns at 0.1 "$cbr2 start"
$ns at 5.0 "$cbr0 stop"
$ns at 5.0 "$cbr2 stop"

$ns at 6.0 "fim"
$ns run
