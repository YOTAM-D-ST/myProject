class Message:
    pass


class Login(Message):
    def __init__(self, my_id):
        self.my_id = my_id
