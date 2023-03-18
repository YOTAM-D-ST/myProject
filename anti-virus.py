"""
anti virus file
"""
import ctypes
import os
import time
from vuls import *
import tkinter as tk
import tkinter.messagebox as messagebox

USER_NAME = os.getlogin()
LOCATION = "c:\\Users\\{}\\AppData\\Roaming\\Microsoft" \
           "\\Windows\\Start Menu\\Programs\\Startup".format(USER_NAME)
ALERT = "A new file has been transplanted in the startup directory",
"Are you sure you want to proceed?"

INITIAL_FILES = os.listdir(LOCATION)


def main():
    global INITIAL_FILES
    while True:

        files_in_startup_dir = os.listdir(LOCATION)

        new_files = [f for f in files_in_startup_dir if f not in INITIAL_FILES]

        if len(new_files) > NO_LEN:
            root = tk.Tk()
            root.withdraw()

            result = messagebox.askyesno(ALERT)
            if result:
                ok = True
            else:
                ok = False
            if ok is True:
                for f in new_files:
                    # Get a list of all running Python processes
                    processes = \
                        os.popen("tasklist | findstr /i python.exe").read()
                    print(LOCATION + '\\' + f)
                    os.remove(LOCATION + '\\' + f)
                    print(f, "removed")
                    newest_time = RESET
                    newest_proc = RESET

                    # Split the processes into a list
                    processes = processes.split("\n")

                    # Get the last process in the list
                    last_process = processes[LAST_PROCCES]

                    # Split the process into its parts
                    parts = last_process.split()

                    # Get the process ID (PID)
                    pid = parts[SECOND_PARAM]

                    # Kill the process
                    os.kill(int(pid), PROCCES_INDEX)
                    print(f, "killed procces")
                INITIAL_FILES = files_in_startup_dir

        time.sleep(1)


if __name__ == '__main__':
    main()
