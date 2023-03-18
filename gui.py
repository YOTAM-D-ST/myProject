"""
gui file
"""
import string
import threading
import time

import wx

from controller import *
from vuls import *

global sharer
global c
global agents


class SharerThread(threading.Thread):
    """
    creates a thread for each sharer,
    in order to creates multiple shares
    """

    def __init__(self, agent):
        """
        creates the thread and declares the
        agent
        :param agent:
        """
        threading.Thread.__init__(self)
        self.agent = agent

    def run(self):
        """
        creates a controller and sending the
        get screen command
        :return:
        """
        print(threading.current_thread().name, self.name)
        c = Controller()
        c.connect(SERVER_IP, SERVER_PORT)
        print(self.agent)
        # Run the selected command
        c.do("get-screen", self.agent)


class MyFrame(wx.Frame):
    """
    creates the gui
    """

    def __init__(self):
        """
        constructor of the gui
        """
        wx.Frame.__init__(self, None, title="My GUI")
        self.panel = wx.Panel(self)
        self.list = wx.ListBox(self.panel)
        for agent in agents:
            self.list.Append(agent)
        # create a run button that calls the share
        self.button = wx.Button(self.panel, label="Run", pos=(300, 100))
        self.button.Bind(wx.EVT_BUTTON, self.on_button_click)
        # create a button for the version command
        self.button = wx.Button(self.panel, label="version", pos=(100, 300))
        self.button.Bind(wx.EVT_BUTTON, self.on_version_button_click)

        # create a stop button that stops the share
        self.stop_button = wx.Button(self.panel, label="stop", pos=(0, 0))
        self.stop_button.Bind(wx.EVT_BUTTON, self.on_stop_button_click)
        # a place for the string of the version
        self.my_text = wx.StaticText(self.panel, wx.ID_ANY, "", pos=(80, 0))
        self.layout()
        # updates the agent list
        thread = threading.Thread(target=self.update_list)
        thread.start()

    def layout(self):
        """
        defines th layout of the window
        :return:
        """
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.list, 20, wx.ALL, 30)
        sizer.Add(self.button, 0, wx.ALL, 10)
        self.panel.SetSizer(sizer)

    def on_version_button_click(self, event):
        """
        sends the get verion command to the
        controller
        :param event:
        :return:
        """
        agent = self.list.GetStringSelection()
        cont = Controller()
        cont.connect(SERVER_IP, SERVER_PORT)
        # Run the selected command
        version = cont.do("get-version", agent)
        print(version)
        self.my_text.SetLabel(version)

    def on_button_click(self, event):
        """
        makes a sharer and starting the thread
        in order to have the share screen
        :param event:
        :return:
        """
        global sharer
        agent = self.list.GetStringSelection()
        sharer = SharerThread(agent)
        sharer.start()
        # t = threading.Thread(target=self.share_button())
        # t.start()

    def on_stop_button_click(self, event):
        """
        calls the stop share method from the controller
        :param event:
        :return:
        """
        thread = threading.Thread(target=self.stop_share)
        thread.start()

    def stop_share(self):
        """
        stops the share by stopping the while loop
        by changing the value of done
        :return:
        """
        global sharer
        c.stop_share()

    def update_list(self):
        global agents
        c = Controller()  # creates a controller object
        # connects the controller to the server
        c.connect(SERVER_IP, SERVER_PORT)
        while True:
            # get the list of agents from the controller
            new_agents = c.do_get_agents()
            new_agents = [a for a in new_agents
                          if not a.strip(" ").startswith("'controller_")]
            list_len = len(agents)
            time.sleep(1)
            new_list_len = len(new_agents)
            if list_len != new_list_len:
                self.list.Clear()
                agents = [a for a in new_agents if
                          not a.strip(" ").startswith("'controller_")]
                for a in agents:
                    self.list.Append(a)
                print(self.list)


def main():
    """
    creates a controller, connects to the server,
    gets the list of agents from the controller,
    creates a gui and starts the gui
    :return:
    """
    global c
    global agents
    c = Controller()  # creates a controller object
    c.connect(SERVER_IP, SERVER_PORT)  # connects the controller to the server
    agents = c.do_get_agents()  # get the list of agents from the controller
    # remove the 'controller' from the list of agents
    agents = [a for a in agents if
              not a.strip(" ").startswith("'controller_")]

    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
