from __future__ import print_function
import sys
from subprocess import check_output, Popen
from socket import create_connection
from time import sleep


def start_and_use_child():
    print("Parent: starting child.py", file=sys.stderr)
    port = int(check_output([sys.executable, "child.py"]))
    print("Parent: got port", port)

    owning_connection = create_connection(("localhost", port))
    for i in range(5):
        data_connection = create_connection(("localhost", port))
        reader, writer = data_connection.makefile('rb', 1), data_connection.makefile('wb', 1)
        writer.write(b"hello\n")
        assert reader.readline() == b"hello\n"
        sleep(1)
        writer.write(b"done\n")
        assert reader.read() == b"done\n"


if 'worker' in sys.argv:
    start_and_use_child()
elif 'crash' in sys.argv:
    workers = [Popen([sys.executable, sys.argv[0], 'worker']) for _ in range(5)]
    print("Parent: started workers", file=sys.stderr)
    sleep(1)
    for worker in workers:
        worker.kill()
    print("Parent: forcefully killing workers, child should terminate", file=sys.stderr)
    sleep(1)
    print("Parent: exiting", file=sys.stderr)
else:
    workers = [Popen([sys.executable, sys.argv[0], 'worker']) for _ in range(5)]
    print("Parent: started workers, waiting for them", file=sys.stderr)
    for worker in workers:
        worker.wait()
    print("Parent: workers finished, child should terminate", file=sys.stderr)
    sleep(1)
    print("Parent: exiting", file=sys.stderr)
