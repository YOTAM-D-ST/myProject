"""yotam shavit project
    project name: unknown
"""
import pickle
import socket
import struct
import sys

from message import *
from vuls import *


class Client:
    def __init__(self, my_id):
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_id = my_id

    def connect(self, ip, port):
        try:
            self.my_socket.connect((ip, port))
        except socket.error as msg:
            print('Connection failure: %s\n terminating program' % msg)
            sys.exit(1)
        # send connect command with my id
        login_cmd = Login(self.my_id);
        msg = pickle.dumps(login_cmd)
        size = len(msg)
        packed_size = struct.pack("!L", size)
        self.my_socket.send(packed_size + msg)

    def share(self):
        pass


def main():
    c = Client("yotam")
    c.connect(SERVER_IP, SERVER_PORT)


if __name__ == '__main__':
    main()
