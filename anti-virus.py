import os
import time
import ctypes
import psutil

user_name = os.getlogin()
location = "c:\\Users\\{}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup".format(
    user_name)

initial_files = os.listdir(location)

while True:

    files_in_startup_dir = os.listdir(location)

    new_files = [f for f in files_in_startup_dir if f not in initial_files]

    if len(new_files) > 0:
        ctypes.windll.user32.MessageBoxW(0, "Warning",
                                         "A new file has been transplanted in the startup directory", "warning", 1)
        for f in new_files:
            print(location + '\\' + f)
            os.remove(location + '\\' + f)
            print(f, "removed")
            for proc in psutil.process_iter():
                if proc.name() == "python.exe":
                    print(proc.time)
                    # proc.terminate()
                    # print(f, "terminated")
        initial_files = files_in_startup_dir

    time.sleep(1)
