from __future__ import print_function
import os
import sys

read_side_id = int(sys.argv[1])
write_side_id = int(sys.argv[2])
print("Child started with pipe r", read_side_id, "w", write_side_id, file=sys.stderr)
read_side = os.fdopen(read_side_id, "r")
print("Child closing write side id", file=sys.stderr)
os.fdopen(write_side_id, "w").close()
print("Child wating on read", file=sys.stderr)
read_side.read()
print("Child terminating", file=sys.stderr) # You should defenitely see this line
