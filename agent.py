"""yotam shavit project
    project name: unknown
"""
import socket
import sys
import platform
import subprocess
import cv2
import numpy as np
import pyautogui
from message import *

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8841
SEND_TO_SOCKET = 1  # The maximum length of the pending connections queue.
EOF = b'-1'
MSG_LEN_PROTOCOL = 4
# size of sock rcv buffer
SOCK_READ_SIZE = 4096
FIRST_LETTER = 1
LAST_LETTER = -1
EXIT = 1
NUM_OF_EXPECTED_PARAMS = 2
PARAM_NAME_OF_AGENT = 1
FIRSR_L_AGENT = 11
LAST_L_AGENT = -2
WINDOW_PROPERTY = 0
CHUNKS = 1024


# import pickle
# import struct
#
#
# def recv(recv_socket):
#     """
#     the protocol, using pickle and struct libary,
#     gets the header recive the message.
#     returns the message
#     :param recv_socket:
#     :return:
#     """
#     c = recv_socket.recv(1).decode()
#     if c == "":
#         return ''
#     if c == 'g':
#         return 'g'
#     payload_size_header = recv_socket.recv(struct.calcsize("!L"))
#     payload_size = struct.unpack("!L", payload_size_header)[0]
#     # get the rest of the message
#     payload = recv_socket.recv(payload_size)
#     # unpickle the msg into an object
#     response = pickle.loads(payload, encoding="bytes")
#     return response
#
#
# class Message:
#     def __init__(self, msg_id, sender):
#         """
#         basic class
#         :param msg_id:
#         """
#         self.msg_id = msg_id
#         self.sender = sender
#
#     def get_id(self):
#         """
#         returns the id
#         :return:
#         """
#         return self.msg_id
#
#     def pack(self):
#         """
#         packs the message so it
#         culd be send using socket
#         :return:
#         """
#         msg = pickle.dumps(self)
#         size = len(msg)
#         packed_size = struct.pack("!L", size)
#         return 'a'.encode() + packed_size + msg
#
#
# class Login(Message):
#     """
#     login sent to the server to identify
#     """
#
#     def __init__(self, my_id):
#         super().__init__("login", my_id)
#
#
# class Share(Message):
#     """
#     share message nicluding peer
#     """
#
#     def __init__(self, peer, my_id):
#         super().__init__("share", my_id)
#         self.peer = peer
#
#
# class ShareResponse(Message):
#     """
#     confirms the share, used by the server
#     """
#
#     def __init__(self, ok, my_id):
#         super().__init__("share-response", my_id)
#         self.ok = ok
#
#
# class Chat(Message):
#     """
#     in case the agents will chat, currently not in use
#     """
#
#     def __init__(self, msg, peer, my_id):
#         super().__init__("chat", my_id)
#         self.msg = msg
#         self.peer = peer
#
#
# class Frame(Message):
#     """
#     the frame that sent when sharing screen
#     """
#
#     def __init__(self, frame, peer, my_id):
#         super().__init__("frame", my_id)
#         self.frame = frame
#         self.peer = peer
#
#
# class GetAgents(Message):
#     """
#     get agents message, used by controller
#     """
#
#     def __init__(self, my_id):
#         super().__init__("get-agents", my_id)
#
#
# class GetAgentsResponse(Message):
#     """
#     get agents response used by server
#     """
#
#     def __init__(self, agents, my_id):
#         super().__init__("get-agents_response", my_id)
#         self.agents = agents
#
#
# class StopShare(Message):
#     """
#     a message that declare to stop the share screen
#     """
#
#     def __init__(self, agent_name, my_id):
#         super().__init__("stop-share", my_id)
#         self.peer = agent_name
#
#
# class Version(Message):
#     def __init__(self, version, my_id):
#         super().__init__("version", my_id)
#         self.version = version
#         self.peer = "controller_MainThread"
#
#
# class GetVersion(Message):
#     def __init__(self, my_id, agent):
#         super().__init__("get-version", my_id)
#         self.peer = agent
#
#
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
        login_cmd = Login(self.my_id)

        self.my_socket.sendall(login_cmd.pack())

    def recv(self):
        """
        recive response from the server and
        call handle server response method
        :return:
        """
        while True:
            print("waiting for server")
            msg = recv(self.my_socket)
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
            case "get-version":
                self.handle_get_version_response()
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
                              response.sender, self.my_id)
            self.my_socket.sendall(frame_msg.pack())
            confirm = recv(self.my_socket)
            print(confirm.msg_id)
            if confirm.msg_id == "share":
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

    def handle_get_version_response(self):
        operating_system = platform.system()
        if operating_system == "Windows":
            command = "wmic os get caption,version"
            result = subprocess.check_output(command,
                                             shell=True).decode("utf-8")
            version = result.splitlines()[1].strip().split(" ")[-1]
            if version.startswith("10.") and version >= "10.0.19041":
                msg = Version("Your operating system version is up-to-date:"
                              " " + version, self.my_id)
            else:
                msg = Version("Your operating system version is not "
                              "up-to-date: " + version, self.my_id)
        elif operating_system == "Linux":
            command = "lsb_release -d"
            result = subprocess.check_output(command, shell=True).\
                decode("utf-8")
            version = result.split(":")[1].strip()
            if version:
                msg = Version("Your operating system version is "
                              "up-to-date: " + version, self.my_id)
            else:
                msg = ("Your operating system version is "
                       "not up-to-date: " + version, self.my_id)
        else:
            msg = Version("Your operating system is not "
                          "supported by this code", self.my_id)
        self.my_socket.sendall(msg.pack())


def main():
    if len(sys.argv) >= NUM_OF_EXPECTED_PARAMS:
        a = Agent(sys.argv[PARAM_NAME_OF_AGENT])
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
    if len(sys.argv) > NUM_OF_EXPECTED_PARAMS:
        a.share(sys.argv[NUM_OF_EXPECTED_PARAMS])
    a.recv()


if __name__ == '__main__':
    main()
