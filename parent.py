from __future__ import print_function

import sys
from subprocess import Popen, PIPE
from time import sleep

python = sys.executable
print("Parent starting child", file=sys.stderr)
child = Popen([python, "child.py"], stdout=PIPE, stdin=PIPE)
port = child.stdout.readline()
print("Parent received port number from child:", port, file=sys.stderr)
print("Parent goes to sleep", file=sys.stderr)
sleep(2)
if len(sys.argv) == 2 and sys.argv[1] == "crash":
    print("Parent crashing", file=sys.stderr)
    raise Exception
else:
    print("Parent closing child's stdin", file=sys.stderr)
    child.stdin.close()
    print("Parent sleeps", file=sys.stderr)
    sleep(0.1)
    print("Parent exiting", file=sys.stderr)
