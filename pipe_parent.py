from __future__ import print_function
import os
import sys
from subprocess import Popen
from time import sleep

read_side_id, write_side_id = os.pipe()
print("Parent created pipe: r", read_side_id, "w", write_side_id, file=sys.stderr)
write_file_object = os.fdopen(write_side_id, "w")
if sys.version_info[0] > 2:
    os.set_inheritable(read_side_id, True)
    os.set_inheritable(write_side_id, True)

python = sys.executable
print("Parent starting child", file=sys.stderr)
child = Popen([python, "pipe_child.py", str(read_side_id), str(write_side_id)], close_fds=False)
print("Parent goes to sleep", file=sys.stderr)
sleep(1)
if len(sys.argv) == 2 and sys.argv[1] == "crash":
    print("Parent crashing", file=sys.stderr)
    raise Exception
else:
    print("Parent closing write side", file=sys.stderr)
    write_file_object.close()
    print("Parent waiting on child", file=sys.stderr)
    child.wait()
    print("Parent exiting", file=sys.stderr)
