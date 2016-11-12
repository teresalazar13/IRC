if {$argc == 5} {
    set cenario [lindex $argv 0]
    set protocol [lindex $argv 1]
    set window [lindex $argv 2]
    set break [lindex $argv 3]
    set speed [lindex $argv 4]
} else {
    puts "Error"
    puts "Usage: argv0 cenario"
    puts "Usage: argv1 protocol"
    puts "Usage: argv2 window"
    puts "Usage: argv3 break"
    puts "Usage: argv4 speed"
    exit 1
}

# Create the 'Simulator' object
set ns [new Simulator]

# Set Dynamic Routing Protocol
$ns rtproto LS

# Open a file for writing the nam trace data
set nf [open out.nam w]
$ns namtrace-all $nf

set nt [open out.tr w]
$ns trace-all $nt

# Add a 'finish' procedure that closes the trace and starts nam
proc finish {} {
    global ns nt
    global ns nf
    $ns flush-trace
    close $nt
    close $nf
    exec nam out.nam
    exit 0
}

# Nodes creation
for {set i 0} {$i < 8} {incr i} {
    set n$i [$ns node]
}

# Links
$ns duplex-link $n0 $n1 $speed 10ms DropTail
$ns duplex-link $n1 $n2 10Mb 10ms DropTail
$ns simplex-link $n1 $n4 10Mb 5ms DropTail
$ns duplex-link $n2 $n3 10Mb 10ms DropTail
$ns duplex-link $n2 $n5 10Mb 10ms DropTail
$ns duplex-link $n3 $n6 10Mb 10ms DropTail
$ns duplex-link $n4 $n5 10Mb 10ms DropTail
$ns duplex-link $n5 $n6 10Mb 10ms DropTail
$ns duplex-link $n5 $n7 10Mb 10ms DropTail

# Nodes' layout
$ns duplex-link-op $n0 $n1 orient right
$ns duplex-link-op $n1 $n2 orient right
$ns simplex-link-op $n1 $n4 orient down
$ns duplex-link-op $n2 $n3 orient right
$ns duplex-link-op $n2 $n5 orient down
$ns duplex-link-op $n3 $n6 orient down
$ns duplex-link-op $n4 $n5 orient right
$ns duplex-link-op $n5 $n6 orient right
$ns duplex-link-op $n5 $n7 orient down

# Packets' colors
$ns color 1 Blue
$ns color 2 Red
$ns color 3 Green

# Shapes
$n0 shape "hexagon"
$n1 shape "square"
$n5 shape "square"
$n7 shape "hexagon"

# Nodes' colors
$n0 color Blue
$n1 color Red
$n5 color Green
$n7 color Blue

# Labels
$n0 label "PC A"
$n1 label "PC B"
$n2 label "PC C"
$n3 label "R3"
$n4 label "R4"
$n5 label "PC D"
$n6 label "R6"
$n7 label "PC E"

# Queue limit
set queue0_1 [[$ns link $n0 $n1] queue]
$queue0_1 set limit_ 2098

set cbr0 [new Application/Traffic/CBR]
$cbr0 set packetSize_ 2097152
$cbr0 set maxpkts_ 1

set null0 [new Agent/Null]
$ns attach-agent $n7 $null0

if {$protocol == "udp"} {
    set udp0 [new Agent/UDP]
    $ns attach-agent $n0 $udp0
    $cbr0 attach-agent $udp0
    $ns connect $udp0 $null0
    $udp0 set class_ 1
}
if {$protocol == "tcp"} {
    set tcp0 [$ns create-connection TCP $n0 TCPSink $n7 1]
    $tcp0 set window_ $window
    $ns attach-agent $n0 $tcp0
    $cbr0 attach-agent $tcp0
}

if {$cenario == 2} {
    set udp1 [new Agent/UDP]
    $ns attach-agent $n1 $udp1

    set cbr1 [new Application/Traffic/CBR]
    $cbr1 set rate_ 6Mb
    $cbr1 attach-agent $udp1

    set null1 [new Agent/Null]
    $ns attach-agent $n5 $null1
    $ns connect $udp1 $null1

    $udp1 set class_ 2

    $ns at 0.5 "$cbr1 start"
  	$ns at 6.0 "$cbr1 stop"


    set udp2 [new Agent/UDP]
    $ns attach-agent $n5 $udp2

    set cbr2 [new Application/Traffic/CBR]
    $cbr2 set rate_ 5Mb
    $cbr2 attach-agent $udp2

    set null2 [new Agent/Null]
    $ns attach-agent $n2 $null2
    $ns connect $udp2 $null2

    $udp2 set class_ 3

    $ns at 0.5 "$cbr2 start"
    $ns at 6.0 "$cbr2 stop"
}

if {$break == 1} {
    #start at 0.5 seconds down 0.75 seconds after and up again 0.9 seconds after start
    $ns rtmodel-at 1.25 down $n2 $n5
    $ns rtmodel-at 1.40 up $n2 $n5
}

$ns at 0.5 "$cbr0 start"
$ns at 6.0 "finish"

# Start the simulation
$ns run
