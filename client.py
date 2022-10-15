"""yotam shavit project
    project name: unknown
"""
import socket
import sys

import cv2
import numpy as np
import pyautogui

import message
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
        self.my_socket.sendall(packed_size + msg)

    def recv(self):
        while True:
            print("waiting for server")
            msg = message.recv(self.my_socket)
            self.handle_server_response(msg)

    def share(self, peer):
        share_cmd = Share(peer);
        self.my_socket.sendall(share_cmd.pack())
        # get the header that includes the size of the rest of the message
        response = message.recv(self.my_socket)
        # handle it
        self.handle_server_response(response)
        self.stream_screen(peer)

    def handle_server_response(self, response):
        msg_id = response.get_id()
        print("got server response ", msg_id)
        match msg_id:
            case "share-response":
                self.handle_share_response(response)
            case "chat":
                self.handle_chat_response(response)
            case "frame":
                self.handle_frame_response(response)
            case _:
                print("unknown msg: " + msg_id)

    def handle_share_response(self, response):
        print("share response: ", response.ok)
        if response.ok:
            while True: # TODO: when to stop ?
                screen = pyautogui.screenshot()
                frame = np.array(screen)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (1024, 576),  # TODO: constants
                                   interpolation=cv2.INTER_AREA)
                result, frame = cv2.imencode('.jpg', frame,
                                             [int(cv2.IMWRITE_JPEG_QUALITY),
                                              90])  # TODO: constants
                frame_msg = Frame(frame,
                                  sys.argv[2])  # TODO: get peer from someplace
                self.my_socket.sendall(frame_msg.pack())
                # TODO: handle exceptions

    def handle_chat_response(self, response):
        print("chat msg ", response.msg)

    def handle_frame_response(self, response):
        frame = response.frame
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        cv2.imshow("hello", frame)

    def stream_screen(self, peer):
        msg = Chat("hello", peer)
        self.my_socket.sendall(msg.pack())


def main():
    c = Client(sys.argv[1])
    print("client ", c.my_id)
    print(len(sys.argv))
    c.connect(SERVER_IP, SERVER_PORT)
    if len(sys.argv) > 2:
        c.share(sys.argv[2])
    c.recv()


if __name__ == '__main__':
    main()
