if {$argc == 1} {
    set window [lindex $argv 0]
} else {
    puts "Error"
    puts "Usage: $argv0 window"
    exit 1
}

set ns [new Simulator]

$ns color 1 Pink
$ns color 2 Orange

$ns color 3 Red
$ns color 4 Blue

set nf [open sim.nam w]
$ns namtrace-all $nf

proc fim {} {
  global ns nf
  $ns flush-trace
  close $nf
  exec nam sim.nam
  exit 0;
}

set n0 [$ns node]
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]

set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]
set n7 [$ns node]

# BERLIM --- PARIS
$ns duplex-link $n0 $n1 13.32Mb 4.392ms DropTail
# PARIS --- MADRID
$ns duplex-link $n1 $n2 40Mb 5.2705ms DropTail
# MADRID --- COIMBRA
$ns duplex-link $n2 $n3 320Mb 2.5645ms DropTail

$ns duplex-link $n4 $n5 13.32Mb 4.392ms DropTail
$ns duplex-link $n5 $n6 40Mb 5.2705ms DropTail
$ns duplex-link $n6 $n7 320Mb 2.5645ms DropTail

# UDP
# BERLIM
set udp0 [new Agent/UDP]
$ns attach-agent $n0 $udp0

set cbr0 [new Application/Traffic/CBR]
$cbr0 set packetSize_ 1024
$cbr0 set maxpkts_ 30
$cbr0 set interval_ 0.01
$cbr0 attach-agent $udp0

# COIMBRA
set null0 [new Agent/Null]
$ns attach-agent $n3 $null0

$ns connect $udp0 $null0

# PARIS
set udp1 [new Agent/UDP]
$ns attach-agent $n1 $udp1

set cbr1 [new Application/Traffic/CBR]
$cbr1 set rate_ 28000000
$cbr1 attach-agent $udp1

# MADRID
set null1 [new Agent/Null]
$ns attach-agent $n2 $null1

$ns connect $udp1 $null1

# TCP
# PARIS
set udp2 [new Agent/UDP]
$ns attach-agent $n5 $udp2

set cbr2 [new Application/Traffic/CBR]
$cbr2 set rate_ 28000000
$cbr2 attach-agent $udp2

# MADRID
set null2 [new Agent/Null]
$ns attach-agent $n6 $null2

$ns connect $udp2 $null2

# BERLIM -> COIMBRA
set tcp0 [$ns create-connection TCP/RFC793edu $n4 TCPSink $n7 1]
$tcp0 set window_ $window

set cbr3 [new Application/Traffic/CBR]
$cbr3 set packetSize_ 1024
$cbr3 set maxpkts_ 30
$cbr3 set interval_ 0.01
$cbr3 attach-agent $tcp0


$ns at 0.0 "$cbr0 start"
$ns at 0.0 "$cbr1 start"
$ns at 0.0 "$cbr2 start"
$ns at 0.0 "$cbr3 start"

$ns at 2 "$cbr3 stop"
$ns at 2 "$cbr0 stop"
$ns at 2 "$cbr1 stop"
$ns at 2 "$cbr2 stop"

$udp0 set class_ 1
$udp1 set class_ 2
$tcp0 set class_ 3
$udp2 set class_ 4

$ns at 2 "fim"

$ns run
