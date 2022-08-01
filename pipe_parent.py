import os
import sys
from subprocess import Popen
from time import sleep

read_side_id, write_side_id = os.pipe()
print("Parent created pipe: r", read_side_id, "w", write_side_id)
write_file_object = os.fdopen(write_side_id)
os.set_inheritable(read_side_id, True)

python = sys.executable
print("Parent starting child")
child = Popen([python, "pipe_child.py", str(read_side_id)], close_fds=False)
print("Parent goes to sleep")
sleep(1)
if len(sys.argv) == 2 and sys.argv[1] == "crash":
    print("Parent crashing")
    raise Exception
else:
    print("Parent closing write side")
    write_file_object.close()
    print("Parent exiting")