from __future__ import print_function
import os
import sys
from subprocess import Popen, PIPE
from time import sleep

read_side_id, write_side_id = os.pipe()
print("Parent created pipe: r", read_side_id, "w", write_side_id, file=sys.stderr)
write_file_object = os.fdopen(write_side_id, "w")
if sys.version_info[0] > 2:
    print("Parent makes pipe descriptors inheritable", file=sys.stderr)
    os.set_inheritable(read_side_id, True)
    os.set_inheritable(write_side_id, True)

if sys.platform == "win32":
    import msvcrt
    from ctypes import windll
    from ctypes.wintypes import DWORD
    read_side_handle = msvcrt.get_osfhandle(read_side_id)
    write_side_handle = msvcrt.get_osfhandle(write_side_id)
    windll.kernel32.SetHandleInformation(read_side_handle, DWORD(1), DWORD(1))
    windll.kernel32.SetHandleInformation(write_side_handle, DWORD(1), DWORD(1))
else:
    read_side_handle, write_side_handle = read_side_id, write_side_id
print("Parent pipe handles: r", read_side_handle, "w", write_side_handle, file=sys.stderr)

print("Parent starting child", file=sys.stderr)
if sys.argv[1] == "py":
    child_cmd = [sys.executable, "pipe_child.py"]
else:
    child_cmd = ["node", "pipe_child.js"]

child = Popen(child_cmd + [str(read_side_handle), str(write_side_handle)], stdout=PIPE, close_fds=False)
print("Parent started the child, reading the port number", file=sys.stderr)
port = int(child.stdout.readline())
print("Parent received port number from child:", port, file=sys.stderr)
print("Parent goes to sleep", file=sys.stderr)
sleep(1)
if len(sys.argv) == 3 and sys.argv[2] == "crash":
    print("Parent crashing", file=sys.stderr)
    raise Exception
else:
    print("Parent closing write side", file=sys.stderr)
    write_file_object.close()
    print("Parent waiting on child", file=sys.stderr)
    child.wait()
    print("Parent exiting", file=sys.stderr)
