"""
yotam sahvit project server
project name: unknown
"""
from vidstream import StreamingServer
import threading

receiver = StreamingServer('172.29.236.26', 9999, 1)

t = threading.Thread(target=receiver.start_server)
t.start()

while input("") != "STOP":
    continue

receiver.stop_server()