import sys

print("Child started", file=sys.stderr)
print("27042")  # port number
print("Child waits on it's input closed", file=sys.stderr)
try:
    input()
except EOFError:
    print("Child got EOF", file=sys.stderr)
print("Child exiting", file=sys.stderr)
