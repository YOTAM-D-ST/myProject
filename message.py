class Message:
    def __init__(self, msg_id):
        self.msg_id = msg_id

    def get_id(self):
        return self.msg_id


class Login(Message):
    def __init__(self, my_id):
        super().__init__("login")
        self.my_id = my_id


class Share(Message):
    def __init__(self, peer_id):
        super().__init__("share")
        self.peer_id = peer_id
