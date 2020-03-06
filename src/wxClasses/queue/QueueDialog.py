# QueueDialog.py
import wx
import logging

from handlers.Data import DataHandler
from wxClasses.queue.PendingPanel import PendingPanel
from wxClasses.queue.HistoryPanel import HistoryPanel


class QueueDialog(wx.Dialog):

    def __init__(self, parent, data):

        wx.Dialog.__init__(self, parent, title='ADI Queue',
                           pos=wx.DefaultPosition,
                           size=(600, 400),
                           style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)

        self.parent: wx.Frame = parent
        self.data: DataHandler = data

        self._create_widgets()

        self.Center()
        self.Show()

    def _create_widgets(self):
        self.notebook = wx.Notebook(self)
        self.pending_panel = PendingPanel(self.notebook, self.data)
        self.history_panel = HistoryPanel(self.notebook, self.data)

        self.notebook.AddPage(self.pending_panel, 'Pending')
        self.notebook.AddPage(self.history_panel, 'History')
