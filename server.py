"""
yotam sahvit project server
project name: unknown
"""
import pickle
import socket
import struct
import sys

from vuls import *


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_running = True


    def bind(self):
        try:
            self.server_socket.bind((self.ip, self.port))
        except socket.error as msg:
            print('Connection failure: %s\n terminating program' % msg)
            sys.exit(1)

    def listen(self):
        self.server_socket.listen(SEND_TO_SOCKET)

    def accept(self):
        done = False
        while done is False:
            client, _ = self.server_socket.accept()
            self.handle_client(client)
        self.server_socket.close()

    def run(self):
        self.bind()
        self.listen()
        self.accept()
        self.is_running = True

    def handle_client_msg(self, msg):
        msg_id = msg.get_id()
        match msg_id:
            case "login":
                self.handle_login(msg)
            case _:
                print("unknown msg: " + msg_id)

    def handle_client(self, client_socket):
        while self.is_running:
            # get the header that includes the size of the rest of the message
            payload_size_header = client_socket.recv(struct.calcsize("!L"))
            payload_size = struct.unpack("!L", payload_size_header)[0]
            # get the rest of the message
            payload = client_socket.recv(payload_size)
            # unpickle the msg into an object
            msg = pickle.loads(payload)
            # handle it
            self.handle_client_msg(msg)
            self.is_running = False

    def handle_login(self, msg):
        print("login from " + msg.my_id)


def main():
    s = Server("0.0.0.0", SERVER_PORT)
    s.run()

if __name__ == '__main__':
    main()