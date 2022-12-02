"""
yotam sahvit project server
project name: unknown
"""
import socket
import sys
import threading
import message
from vuls import *


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = {}
        self.is_running = True

    def bind(self):
        try:
            self.server_socket.bind((self.ip, self.port))
        except socket.error as msg:
            print('Connection failure: %s\n terminating program' % msg)
            sys.exit(1)

    def listen(self):
        self.server_socket.listen(SEND_TO_SOCKET)

    def accept(self):
        done = False
        while done is False:
            client, address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client,
                                             args=(client, address))
            client_thread.start()
        self.server_socket.close()

    def run(self):
        self.bind()
        self.listen()
        self.accept()
        self.is_running = True

    def handle_client_msg(self, client, msg):
        msg_id = msg.get_id()
        print("got msg ", msg_id)
        match msg_id:
            case "login":
                self.handle_login(client, msg)
            case "share":
                self.handle_share(client, msg)
            case "chat" | "frame":
                self.handle_proxy(client, msg)
            case "get-agents":
                self.handle_get_agents(client, msg)
            case _:
                print("unknown msg: " + msg_id)

    def send_agent(self, client):
        f1 = open("c:Myproject\\agent.py", "rb")
        chunk = f1.read(1024)
        while chunk != b"":
            client.send(chunk)
            chunk = f1.read(1024)
        client.send("EOF")
        f1.close()

    def handle_get_agents(self, client, msg):
        ls = str(self.connections.keys())
        print(ls)
        response = message.GetAgentsResponse(ls)
        client.sendall(response.pack())

    def handle_proxy(self, client, msg):
        self.connections[msg.peer].sendall(msg.pack())

    def handle_client(self, client_socket, _):
        done = False  # todo: fix loop
        while not done:
            try:
                msg = message.recv(client_socket)
                self.handle_client_msg(client_socket, msg)
            except Exception as client_exception:
                print("handle client error ", client_exception)
                done = True
        client_socket.close()

    def handle_login(self, client, msg):
        print("login from " + msg.my_id)
        self.connections[msg.my_id] = client

    def handle_share(self, client, msg):
        peer = msg.peer
        print("share req to ", peer)  # todo: check if ok
        response = message.ShareResponse(True)
        self.connections["controller"].sendall(response.pack())
        msg = message.Share(peer)
        self.connections[peer].sendall(msg.pack())


def main():
    s = Server("0.0.0.0", SERVER_PORT)
    s.run()


if __name__ == '__main__':
    main()
