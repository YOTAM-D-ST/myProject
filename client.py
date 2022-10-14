"""yotam shavit project
    project name: unknown
"""
import threading

from vidstream import ScreenShareClient #libary for screen share

sender = ScreenShareClient("172.29.236.26", 9999)

t = threading.Thread(target=sender.start_stream)
t.start()

while input("") != "STOP":
    continue

sender.stop_stream()
