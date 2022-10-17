import sys

import client
import message
from vuls import *


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
        self.send(message.GetAgents)
        response = message.recv(self.my_socket)
        print(response.agents)


def main():
    c = Controller()
    c.connect(SERVER_IP, SERVER_PORT)
    c.do(sys.argv[1])


if __name__ == '__main__':
    main()
