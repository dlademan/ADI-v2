import wx
import logging

from Handlers.Data import DataHandler
from wxObjects.OLVPanel import OLVPanel
from wxObjects.TreePanel import TreePanel


class NotebookPanel(wx.Notebook):

    def __init__(self, parent, data: DataHandler):
        wx.Notebook.__init__(self, parent)

        self.notebook_library = wx.Notebook(self)
        self.tree_panel: TreePanel = TreePanel(self.notebook_library, data)
        self.olv_panel: OLVPanel = OLVPanel(self.notebook_library, data)

        self.notebook_library.AddPage(self.tree_panel, 'Tree')
        self.notebook_library.AddPage(self.olv_panel, 'List')

        left_box = wx.BoxSizer(wx.VERTICAL)
        left_box.Add(self.notebook_library, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(left_box)
