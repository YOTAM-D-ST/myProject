import string

import wx

from controller import *
from vuls import *

global sharer
global c
global agents


class SharerThread(threading.Thread):
    def __init__(self, agent):
        threading.Thread.__init__(self)
        self.agent = agent

    def run(self):
        print(threading.current_thread().name, self.name)
        c = Controller()
        c.connect(SERVER_IP, SERVER_PORT)
        print(self.agent)
        # Run the selected command
        c.do("get-screen", self.agent)


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="My GUI")
        self.panel = wx.Panel(self)
        self.commands = agents  # create a list of agents
        self.list = wx.ListBox(self.panel)
        for agent in agents:
            self.list.Append(agent)
            # create a run button that calls the share
        self.button = wx.Button(self.panel, label="Run")
        self.button.Bind(wx.EVT_BUTTON, self.on_button_click)
        # create a stop button that stops the share
        self.stop_button = wx.Button(self.panel, label="stop")
        self.stop_button.Bind(wx.EVT_BUTTON, self.on_stop_button_click)
        self.layout()

    def layout(self):
        """
        defines th layout of the window
        :return:
        """
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.list, 20, wx.ALL, 30)
        sizer.Add(self.button, 0, wx.ALL, 10)
        self.panel.SetSizer(sizer)

    def on_button_click(self, event):
        global sharer
        agent = self.list.GetStringSelection()
        sharer = SharerThread(agent)
        sharer.start()
        # t = threading.Thread(target=self.share_button())
        # t.start()

    def share_button(self):
        # Get the selected command from the choice widget
        agent = self.list.GetStringSelection()
        print(agent, threading.current_thread().name)
        c = Controller()
        c.connect(SERVER_IP, SERVER_PORT)
        print(agent)
        # Run the selected command
        c.do("get-screen", agent)

    def on_stop_button_click(self, event):
        """
        calls the stop share method from the controller
        :param event:
        :return:
        """
        thread = threading.Thread(target=self.stop_share())
        thread.start()

    def stop_share(self):
        global sharer
        c.stop_share()


def main():
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
