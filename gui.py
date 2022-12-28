import doctest
import ctypes
import wx
from controller import *
from vuls import *

c = Controller()
c.connect(SERVER_IP, SERVER_PORT)
agents = c.do_get_agents()


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="My GUI")
        self.panel = wx.Panel(self)
        self.commands = agents
        self.choice = wx.Choice(self.panel, choices=self.commands)
        self.button = wx.Button(self.panel, label="Run")
        self.button.Bind(wx.EVT_BUTTON, self.on_button_click)
        self.layout()

    def layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.choice, 0, wx.ALL, 10)
        sizer.Add(self.button, 0, wx.ALL, 10)
        self.panel.SetSizer(sizer)

    def on_button_click(self, event):
        # Get the selected command from the choice widget
        agent = self.choice.GetStringSelection()
        # Run the selected command
        c.do("get-screen {}".format(agent))


app = wx.App()
frame = MyFrame()
frame.Show()
app.MainLoop()
