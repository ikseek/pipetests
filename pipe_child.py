from __future__ import print_function
import os
import sys

read_side_id = int(sys.argv[1])
print("Child started with pipe", read_side_id)
read_side = os.fdopen(read_side_id, "r")
print("Child wating on read")
read_side.read()
print("Child terminating")