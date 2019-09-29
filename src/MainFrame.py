import wx
from pathlib import Path

from Data import DataHandler


class MainFrame(wx.Frame):
    """
    Main frame window of ADI
    """

    def __init__(self, parent, wx_id, title, debug):

        wx.Frame.__init__(self, parent, wx_id, title,
                          pos=wx.DefaultPosition,
                          size=(1300, 800),
                          style=wx.DEFAULT_FRAME_STYLE)

        self.data: DataHandler = DataHandler(debug)
        self.tree = None
        self.Show()

    def _create_library_tree(self):
        
        return None

    def on_close(self):

        self.data.database.connection.close()
        self.Close()
