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


class Agent:
    def __init__(self, my_id):
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_id = my_id

    def connect(self, ip, port):
        """
        connects to the server then creates
        a login message and sends it
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
        call the pack method, sends to the server
        :param msg:
        :return:
        """
        self.my_socket.sendall(msg.pack())

    def handle_server_response(self, response):
        """
        match response to the correct method
        :param response:
        :return:
        """
        msg_id = response.get_id()
        print("got server response ", msg_id)
        match msg_id:
            case "share":
                self.share(response)
            case "chat":
                self.handle_chat_response(response)
            case "frame":
                self.handle_frame_response(response)
            case _:
                print("unknown msg: " + msg_id)

    def share(self, response):
        """
        method to share the screen , makes frames with cv2
        libary and sends them
        :param response:
        :return:
        """
        done = False
        while not done:  # TODO: when to stop ?
            screen = pyautogui.screenshot()
            frame = np.array(screen)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (1024, 576),  # TODO: constants
                               interpolation=cv2.INTER_AREA)
            result, frame = cv2.imencode('.jpg', frame,
                                         [int(cv2.IMWRITE_JPEG_QUALITY),
                                          90])  # TODO: constants
            frame_msg = Frame(frame,
                              "controller")
            self.my_socket.sendall(frame_msg.pack())
            if message.recv(self.my_socket).msg_id == "share":
                done = False
            else:
                done = True
            # TODO: handle exceptions

    def handle_chat_response(self, response):
        """
        in case the server want to chat with the agent
        :param response:
        :return:
        """
        print("chat msg ", response.msg)

    def handle_frame_response(self, response):
        """
        in case the agent want to recive frames
        :param response:
        :return:
        """
        frame = response.frame
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        cv2.imshow("hello", frame)
        cv2.waitKey(1)


def main():
    if len(sys.argv) >= 2:
        a = Agent(sys.argv[1])
    else:
        try:
            hostname = socket.gethostname()
            recognition = socket.gethostbyname(hostname)
        except Exception as e:
            recognition = "guest"
        a = Agent(recognition)
    print("client ", a.my_id)
    print(len(sys.argv))
    a.connect(SERVER_IP, SERVER_PORT)
    if len(sys.argv) > 2:
        a.share(sys.argv[2])
    a.recv()


if __name__ == '__main__':
    main()
