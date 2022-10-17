import pickle
import struct


def recv(recv_socket):
    payload_size_header = recv_socket.recv(struct.calcsize("!L"))
    payload_size = struct.unpack("!L", payload_size_header)[0]
    # get the rest of the message
    payload = recv_socket.recv(payload_size)
    # unpickle the msg into an object
    response = pickle.loads(payload, encoding="bytes")
    return response


class Message:
    def __init__(self, msg_id):
        self.msg_id = msg_id

    def get_id(self):
        return self.msg_id

    def pack(self):
        msg = pickle.dumps(self)
        size = len(msg)
        packed_size = struct.pack("!L", size)
        return packed_size + msg


class Login(Message):
    def __init__(self, my_id):
        super().__init__("login")
        self.my_id = my_id


class Share(Message):
    def __init__(self, peer):
        super().__init__("share")
        self.peer = peer


class ShareResponse(Message):
    def __init__(self, ok):
        super().__init__("share-response")
        self.ok = ok


class Chat(Message):
    def __init__(self, msg, peer):
        super().__init__("chat")
        self.msg = msg
        self.peer = peer


class Frame(Message):
    def __init__(self, frame, peer):
        super().__init__("frame")
        self.frame = frame
        self.peer = peer


class GetAgents(Message):
    def __init__(self):
        super().__init__("get-agents")


class GetAgentsResponse(Message):
    def __init__(self, agents):
        super().__init__("get-agents_response")
        self.agents = agents

