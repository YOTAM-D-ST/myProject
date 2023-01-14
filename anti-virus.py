import ctypes
import os
import time

user_name = os.getlogin()
location = "c:\\Users\\{}\\AppData\\Roaming\\Microsoft" \
           "\\Windows\\Start Menu\\Programs\\Startup".format(
                user_name)

initial_files = os.listdir(location)

while True:

    files_in_startup_dir = os.listdir(location)

    new_files = [f for f in files_in_startup_dir if f not in initial_files]

    if len(new_files) > 0:
        ctypes.windll.user32.MessageBoxW(0, "Warning",
                                         "A new file has been "
                                         "transplanted in the "
                                         "startup directory",
                                         "warning", 1)
        for f in new_files:
            # Get a list of all running Python processes
            processes = os.popen("tasklist | findstr /i python.exe").read()
            print(location + '\\' + f)
            os.remove(location + '\\' + f)
            print(f, "removed")
            newest_time = 0
            newest_proc = 0

            # Split the processes into a list
            processes = processes.split("\n")

            # Get the last process in the list
            last_process = processes[-2]

            # Split the process into its parts
            parts = last_process.split()

            # Get the process ID (PID)
            pid = parts[1]

            # Kill the process
            os.kill(int(pid), 9)
            print(f, "killed procces")
        initial_files = files_in_startup_dir

    time.sleep(1)
