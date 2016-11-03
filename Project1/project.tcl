if {$argc == 1} {
    set cenario [lindex $argv 0]
} else {
    puts "Error"
    puts "Usage: $argv0 cenario"
    exit 1
}

# Create the 'Simulator' object
set ns [new Simulator]

# Open a file for writing the nam trace data
set nf [open out.nam w]
$ns trace-all $nf

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

set cbr0 [new Application/Traffic/CBR]
$cbr0 set packetSize_ 2048
$cbr0 set maxpkts_ 1
$cbr0 attach-agent $udp0

if {$cenario == 1} {
  set udp0 [new Agent/UDP]
  $ns attach-agent $n0 $udp0
}

if {$cenario == 2} {

}

# Start the simulation
$ns run
