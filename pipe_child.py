import os
import sys

read_side_id = int(sys.argv[1])
print("Child started with pipe", read_side_id)
read_side = os.fdopen(read_side_id)
print("Child wating on read")
read_side.read()
print("Child terminating")