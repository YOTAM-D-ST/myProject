import wx
import threading
from controller import *
from vuls import *

c = Controller()  # creates a controller object
c.connect(SERVER_IP, SERVER_PORT)  # connects the controller to the server
agents = c.do_get_agents()  # get the list of agents from the controller
# remove the 'controller' from the list of agents
if " 'controller'" in agents:
    agents.remove(" 'controller'")
if "'controller'" in agents:
    agents.remove("'controller'")


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
        thread = threading.Thread(target=self.share_button())
        thread.start()

    def share_button(self):
        # Get the selected command from the choice widget
        agent = self.list.GetStringSelection()
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
        c.stop_share()


app = wx.App()
frame = MyFrame()
frame.Show()
app.MainLoop()
