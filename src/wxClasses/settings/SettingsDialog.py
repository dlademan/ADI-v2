import wx
import logging

from handlers.Data import DataHandler
from src.wxClasses.settings.DirectoriesPanel import DirectoriesPanel


class SettingsDialog(wx.Dialog):

    def __init__(self, parent, data):

        wx.Dialog.__init__(self, parent, title='ADI Configuration',
                           pos=wx.DefaultPosition,
                           size=(600, 400),
                           style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)

        self.parent: wx.Frame = parent
        self.data: DataHandler = data

        self._create_widgets()

        self.SetSize(self.GetBestVirtualSize())
        self.Center()
        self.ShowModal()

    def _create_widgets(self):
        self.notebook = wx.Notebook(self)
        self.dir_panel = DirectoriesPanel(self.notebook, self.data)

        self.notebook.AddPage(self.dir_panel, 'Directories')

    def _create_boxes(self):
        title_box = wx.BoxSizer()
        title_box.Add(0, 0, 1)
        # title_box.Add(self.title_label, 0, wx.EXPAND | wx.ALL)
        title_box.Add(0, 0, 1)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(title_box, 0, wx.EXPAND | wx.RIGHT, 5)
        box.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(box)

    def _create_binds(self):
        self.Bind(wx.EVT_BUTTON, self._on_close, self.dir_panel.close_button)
        self.Bind(wx.EVT_CLOSE, self._on_close)

    def _on_close(self):
        logging.info('SettingsDialog Closed')
        self.Destroy()
