import wx

from controller import *
from vuls import *

c = Controller()
c.connect(SERVER_IP, SERVER_PORT)
agents = c.do_get_agents()
if " 'controller'" in agents:
    agents.remove(" 'controller'")
if "'controller'" in agents:
    agents.remove("'controller'")


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="My GUI")
        self.panel = wx.Panel(self)
        self.commands = agents
        self.list = wx.ListBox(self.panel)
        for agent in agents:
            self.list.Append(agent)
        self.button = wx.Button(self.panel, label="Run")
        self.button.Bind(wx.EVT_BUTTON, self.on_button_click)
        self.stop_button = wx.Button(self.panel, label="stop")
        self.stop_button.Bind(wx.EVT_BUTTON, self.on_stop_button_click)
        self.layout()

    def layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.list, 20, wx.ALL, 30)
        sizer.Add(self.button, 0, wx.ALL, 10)
        self.panel.SetSizer(sizer)

    def on_button_click(self, event):
        # Get the selected command from the choice widget
        agent = self.list.GetStringSelection()
        print(agent)
        # Run the selected command
        c.do("get-screen", agent)

    def on_stop_button_click(self, event):
        c.stop_share()


app = wx.App()
frame = MyFrame()
frame.Show()
app.MainLoop()
