"""
yotam sahvit project server
project name: unknown
"""
import socket
import sys
from vuls import *

class Server:
    def __init__(self, ip, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, ip, port):
        try:
            self.server_socket.bind((ip, port))
            self.server_socket.listen(SEND_TO_SOCKET)
        except socket.error as msg:
            print('Connection failure: %s\n terminating program' % msg)
            sys.exit(1)

