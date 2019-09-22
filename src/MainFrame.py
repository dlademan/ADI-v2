import wx
from pathlib import Path

from Data import DataHandler


class MainFrame(wx.Frame):
    """
    Main frame window of ADI
    """

    def __init__(self, parent, wx_id, title):

        wx.Frame.__init__(self, parent, wx_id, title,
                          pos=wx.DefaultPosition,
                          size=(1300, 800),
                          style=wx.DEFAULT_FRAME_STYLE)

        self.data = DataHandler()
        self.Show()
