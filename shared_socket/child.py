from __future__ import print_function
import sys
import os
from threading import Lock
from subprocess import Popen
from time import sleep

try:
    from socketserver import ThreadingTCPServer, StreamRequestHandler
    from subprocess import DEVNULL
except ImportError:
    from SocketServer import ThreadingTCPServer, StreamRequestHandler

    DEVNULL = open(os.devnull, 'w')
    FileExistsError = OSError
    FileNotFoundError = IOError


class EchoServer(ThreadingTCPServer):
    allow_reuse_address = True
    request_queue_size = 100
    active_clients = 0
    active_clients_lock = Lock()

    def __init__(self, address):
        ThreadingTCPServer.__init__(self, address, EchoRequest)


class EchoRequest(StreamRequestHandler):
    def handle(self):
        with EchoServer.active_clients_lock:
            EchoServer.active_clients += 1

        try:
            for line in self.rfile:
                self.wfile.write(line)
                if line == b'done\n':
                    break
                else:
                    print("Server serving", line.decode().strip(), file=sys.stderr)
        except BaseException as e:
            print("Child: client failed with", e, file=sys.stderr)

        with EchoServer.active_clients_lock:
            EchoServer.active_clients -= 1
            last_client_gone = EchoServer.active_clients == 0
        if last_client_gone:
            print("Child: last client gone, terminating", file=sys.stderr)
            self.server.shutdown()


if 'serve' in sys.argv:
    try:
        portfile = os.open('child.port', os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        try:
            server = EchoServer(("localhost", 2222))
            print("Child: started server on port 2222", file=sys.stderr)
            os.write(portfile, b'2222\n')
            sleep(1)
            server.serve_forever()
            print("Child: quit server on port 2222", file=sys.stderr)
        finally:
            os.remove('child.port')
    except FileExistsError:
        pass
else:
    if not os.path.exists('child.port'):
        Popen([sys.executable, sys.argv[0], "serve"], stdout=DEVNULL)
    port = None
    while not port:
        try:
            sleep(0.1)
            with open('child.port', 'r') as portfile:
                port = portfile.readline()
        except FileNotFoundError:
            pass
    print(port)
    sys.stdout.flush()
