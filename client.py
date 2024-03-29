"""
client file
"""
import pickle
import socket
import struct
import sys

import message


class Client:
    """
    client class
    """
    def __init__(self, my_id):
        """
        instructor
        :param my_id:
        """
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_id = my_id

    def connect(self, ip, port):
        """
        connects to the server and makes
        a login nessage
        :param ip:
        :param port:
        :return:
        """
        try:
            self.my_socket.connect((ip, port))
        except socket.error as msg:
            print('Connection failure: %s\n terminating program' % msg)
            sys.exit(1)
        # send connect command with my id
        login_cmd = message.Login(self.my_id)
        self.my_socket.sendall(login_cmd.pack())

    def recv(self):
        """
        recive response from the server and
        call handle server response method
        :return:
        """
        while True:
            print("waiting for server")
            msg = message.recv(self.my_socket)
            self.handle_server_response(msg)

    def send(self, msg):
        """
        sending the msg to the server
        :param msg:
        :return:
        """
        self.my_socket.sendall(msg.pack())
