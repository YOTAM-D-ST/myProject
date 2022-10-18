import pickle
import socket
import struct
import sys

import message


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
        login_cmd = message.Login(self.my_id)
        msg = pickle.dumps(login_cmd)
        size = len(msg)
        packed_size = struct.pack("!L", size)
        self.my_socket.sendall(packed_size + msg)

    def recv(self):
        while True:
            print("waiting for server")
            msg = message.recv(self.my_socket)
            self.handle_server_response(msg)

    def send(self, msg):
        self.my_socket.sendall(msg.pack())
