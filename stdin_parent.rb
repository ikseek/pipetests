STDERR.puts "Parent starting child"
in_r, in_w = IO.pipe()
out_r, out_w = IO.pipe()
child = spawn("node", "stdin_child.js", :in=>in_r, :out=>out_w)
STDERR.puts "Parent started the child, reading the port number"
port = out_r.readline
STDERR.print "Parent received port number from child: ", port
STDERR.puts "Parent goes to sleep"
sleep 2
if ARGV.length == 1 and ARGV[0] == "crash"
    STDERR.puts "Parent crashing"
    Process.kill("SEGV", Process.pid)
    STDERR.puts "Parent should not print it, should crash"
else
    STDERR.puts "Parent closing child's stdin"
    in_w.close
    STDERR.puts "Parent waits for child to exit"
    Process.wait child
    STDERR.puts "Parent exiting"
end
