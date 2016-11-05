if {$argc == 2} {
    set cenario [lindex $argv 0]
    set protocol "tcp"
    set window [lindex $argv 1]
} elseif {$argc == 1} {
    set cenario [lindex $argv 0]
    set protocol "udp"
} else {
    puts "Error"
    puts "Usage: $argv0 cenario"
    puts "Usage: $argv1 protocol"
    puts "Usage: $argv2 window"
    exit 1
}

# Create the 'Simulator' object
set ns [new Simulator]

$ns color 1 Pink

# Open a file for writing the nam trace data
set nf [open out.nam w]
$ns namtrace-all $nf

# Add a 'finish' procedure that closes the trace and starts nam
proc finish {} {
    global ns nf
    $ns flush-trace
    close $nf
    exec nam out.nam &
    exit 0
}

# Create nodes
for {set i 0} {$i < 8} {incr i} {
    set n$i [$ns node]
}

# Link
$ns duplex-link $n0 $n1 10Mb 10ms DropTail
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

set cbr0 [new Application/Traffic/CBR]
$cbr0 set packetSize_ 2048
$cbr0 set maxpkts_ 1

set null0 [new Agent/Null]
$ns attach-agent $n7 $null0

if {$cenario == 1} {
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
    $cbr0 attach-agent $tcp0
  }
}

if {$cenario == 2} {

}

$ns at 0.5 "$cbr0 start"
$ns at 6.0 "finish"


# Start the simulation
$ns run