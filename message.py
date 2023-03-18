"""
messages file
"""
import pickle
import struct

RECIVER = 1


def recv(recv_socket):
    """
    the protocol, using pickle and struct libary,
    gets the header recive the message.
    returns the message
    :param recv_socket:
    :return:
    """
    c = recv_socket.recv(RECIVER).decode()
    print(c)
    if c == "":
        return ''
    if c == 'g':
        return 'g'
    payload_size_header = recv_socket.recv
    payload_size = struct.unpack("!L", payload_size_header)[0]
    # get the rest of the message
    payload = recv_socket.recv(payload_size)
    while True:
        if len(payload) == payload_size:
            break
        payload += recv_socket.recv(payload_size)

    if len(payload) != payload_size:
        # log the error or raise an exception with a custom message
        print("Error: received payload ", len(payload),
              " size does not match expected size ", payload_size)
        return None
    # unpickle the msg into an object
    response = pickle.loads(payload, encoding="bytes")
    return response


class Message:
    def __init__(self, msg_id, sender):
        """
        basic class
        :param msg_id:
        """
        self.msg_id = msg_id
        self.sender = sender

    def get_id(self):
        """
        returns the id
        :return:
        """
        return self.msg_id

    def pack(self):
        """
        packs the message so it
        culd be send using socket
        :return:
        """
        msg = pickle.dumps(self)
        size = len(msg)
        packed_size = struct.pack("!L", size)
        return 'a'.encode() + packed_size + msg


class Login(Message):
    """
    login sent to the server to identify
    """

    def __init__(self, my_id):
        """
        constructor
        :param my_id:
        """
        super().__init__("login", my_id)


class Share(Message):
    """
    share message nicluding peer
    """

    def __init__(self, peer, my_id):
        """
                constructor
                :param my_id:
                """
        super().__init__("share", my_id)
        self.peer = peer


class ShareResponse(Message):
    """
    confirms the share, used by the server
    """

    def __init__(self, ok, my_id):
        """
        constructor
        :param my_id:
        """
        super().__init__("share-response", my_id)
        self.ok = ok


class Chat(Message):
    """
    in case the agents will chat, currently not in use
    """

    def __init__(self, msg, peer, my_id):
        """
        constructor
        :param my_id:
        """
        super().__init__("chat", my_id)
        self.msg = msg
        self.peer = peer


class Frame(Message):
    """
    the frame that sent when sharing screen
    """

    def __init__(self, frame, peer, my_id):
        """
        constructor
        :param my_id:
    """
        super().__init__("frame", my_id)
        self.frame = frame
        self.peer = peer


class GetAgents(Message):
    """
    get agents message, used by controller
    """

    def __init__(self, my_id):
        """
        construct
        :param my_id:
        """
        super().__init__("get-agents", my_id)


class GetAgentsResponse(Message):
    """
    get agents response used by server
    """

    def __init__(self, agents, my_id):
        """
        construct
        :param agents:
        :param my_id:
        """
        super().__init__("get-agents_response", my_id)
        self.agents = agents


class StopShare(Message):
    """
    a message that declare to stop the share screen
    """

    def __init__(self, agent_name, my_id):
        """
        construct
        :param agent_name:
        :param my_id:
        """
        super().__init__("stop-share", my_id)
        self.peer = agent_name


class Version(Message):
    """
    a message that commands to return if
    the software is up to date
    """

    def __init__(self, version, my_id):
        """
        constructor
        :param version:
        :param my_id:
        """
        super().__init__("version", my_id)
        self.version = version
        self.peer = "controller_MainThread"


class GetVersion(Message):
    """
    returns the answer for the get verion
    command
    """

    def __init__(self, my_id, agent):
        """
        constructor
        :param my_id:
        :param agent:
        """
        super().__init__("get-version", my_id)
        self.peer = agent
