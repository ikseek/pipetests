from __future__ import print_function
import sys

print("Child started", file=sys.stderr)
print("27042")  # port number
sys.stdout.flush()  # needed on python 2
print("Child waits on it's input closed", file=sys.stderr)
try:
    input()
except EOFError:
    print("Child got EOF", file=sys.stderr)
print("Child exiting", file=sys.stderr)
