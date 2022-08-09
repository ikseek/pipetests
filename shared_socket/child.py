from __future__ import print_function
import sys
import os
from itertools import count
from socketserver import ThreadingTCPServer, StreamRequestHandler
from threading import Lock
from subprocess import Popen, DEVNULL
from time import sleep


class EchoServer(ThreadingTCPServer):
    allow_reuse_address = True
    active_clients = 0
    active_clients_lock = Lock()
    request_count = count()

    def __init__(self, address):
        super(EchoServer, self).__init__(address, EchoServer.Request)

    class Request(StreamRequestHandler):
        def handle(self) -> None:
            print("Child: handling request", next(EchoServer.request_count), file=sys.stderr)
            with EchoServer.active_clients_lock:
                EchoServer.active_clients += 1

            try:
                for line in self.rfile:
                    self.wfile.write(line)
                    if line == b'done\n':
                        break
            except BaseException as e:
                print("Child: client failed with", e, file=sys.stderr)

            with EchoServer.active_clients_lock:
                EchoServer.active_clients -= 1
                last_client_gone = EchoServer.active_clients == 0
            if last_client_gone:
                print("Child: last client gone, terminating", file=sys.stderr)
                self.server.shutdown()


def read_portfile():
    try:
        with open('child.port', 'r') as portfile:
            for _ in range(10):
                line = portfile.read()
                if line:
                    return line
                sleep(0.1)
            else:
                raise Exception("Server didn't output port")
    except FileNotFoundError:
        pass
    return None


if 'serve' in sys.argv:
    try:
        server = EchoServer(("localhost", 2222))
    except OSError:
        exit(0)
    print("Child: started server on port 2222", file=sys.stderr)
    with open('child.port', 'w') as portfile:
        portfile.write("2222")
    try:
        server.serve_forever()
    finally:
        print("Child: quit server on port 2222", file=sys.stderr)
        os.remove('child.port')
else:
    port = read_portfile()
    if not port:
        process = Popen([sys.executable, sys.argv[0], "serve"], stdout=DEVNULL, stdin=DEVNULL)
        while not port:
            sleep(0.1)
            port = read_portfile()
    print(port, flush=True)
