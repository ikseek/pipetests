from __future__ import print_function

import os
import sys
from subprocess import check_output, Popen
from socket import create_connection
from time import sleep

if sys.version_info < (3,):
    ConnectionRefusedError = IOError


def message(text):
    sys.stderr.write(text + "\n")
    sys.stderr.flush()


def start_and_use_child():
    try:
        message("Worker: starting child.py")
        sys.stderr.flush()
        port = int(check_output([sys.executable, "child.py"]))
        owning_connection = create_connection(("localhost", port))
    except ConnectionRefusedError:
        message("Worker: second attempt of starting child.py")
        sys.stderr.flush()
        port = int(check_output([sys.executable, "child.py"]))
        owning_connection = create_connection(("localhost", port))

    for i in range(5):
        data_connection = create_connection(("localhost", port))
        reader, writer = data_connection.makefile('rb', 1), data_connection.makefile('wb', 1)
        msg = b"worker %d test %d\n" % (os.getpid(), i)
        writer.write(msg)
        assert reader.readline() == msg
        sleep(1)
        writer.write(b"done\n")
        assert reader.read() == b"done\n"


if 'worker' in sys.argv:
    start_and_use_child()
else:
    workers = [Popen([sys.executable, sys.argv[0], 'worker']) for _ in range(5)]
    message("Parent: started workers, sleeping")
    if 'kill' in sys.argv:
        sleep(2)
        message("Parent: violently killing all the workers")
        for worker in workers:
            worker.kill()
    else:
        message("Parent: waiting for workers to finish")
        for worker in workers:
            worker.wait()
    message("Parent: workers done, child should terminate")
    sleep(1)
    message("Parent: exiting")
