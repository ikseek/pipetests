from __future__ import print_function

import sys
from subprocess import Popen, PIPE
from time import sleep

print("Parent starting child", file=sys.stderr)
child = Popen(["node", "stdin_child.js"], stdout=PIPE, stdin=PIPE)
print("Parent started the child, reading the port number", file=sys.stderr)
port = int(child.stdout.readline())
print("Parent received port number from child:", port, file=sys.stderr)
print("Parent goes to sleep", file=sys.stderr)
sleep(2)
if len(sys.argv) == 2 and sys.argv[1] == "crash":
    print("Parent crashing", file=sys.stderr)
    raise Exception
else:
    print("Parent closing child's stdin", file=sys.stderr)
    child.stdin.close()
    print("Parent waits for child to exit", file=sys.stderr)
    child.wait()
    print("Parent exiting", file=sys.stderr)
