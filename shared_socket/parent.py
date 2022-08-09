from __future__ import print_function

import os
import sys
from subprocess import check_output, Popen
from socket import create_connection
from time import sleep


def start_and_use_child():
    print("Worker: starting child.py", file=sys.stderr)
    sys.stderr.flush()
    port = int(check_output([sys.executable, "child.py"]))

    owning_connection = create_connection(("localhost", port))
    for i in range(5):
        data_connection = create_connection(("localhost", port))
        reader, writer = data_connection.makefile('rb', 1), data_connection.makefile('wb', 1)
        message = b"worker %d test %d\n" % (os.getpid(), i)
        writer.write(message)
        assert reader.readline() == message
        sleep(1)
        writer.write(b"done\n")
        assert reader.read() == b"done\n"


if 'worker' in sys.argv:
    start_and_use_child()
else:
    workers = [Popen([sys.executable, sys.argv[0], 'worker']) for _ in range(5)]
    print("Parent: started workers, sleeping", file=sys.stderr)
    sleep(1)
    if 'kill' in sys.argv:
        print("Parent: violently killing all the workers", file=sys.stderr)
        for worker in workers:
            worker.kill()
    else:
        print("Parent: waiting for workers to finish", file=sys.stderr)
        for worker in workers:
            worker.wait()
    print("Parent: workers done, child should terminate", file=sys.stderr)
    sleep(1)
    print("Parent: exiting", file=sys.stderr)
