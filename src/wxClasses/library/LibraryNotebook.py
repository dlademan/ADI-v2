import wx

from Handlers.Main import MainHandler
from wxClasses.library.OLVPanel import OLVPanel
from wxClasses.library.TreePanel import TreePanel


class LibraryNotebook(wx.Notebook):

    def __init__(self, parent, data: MainHandler):
        wx.Notebook.__init__(self, parent)

        self.notebook = wx.Notebook(self)
        self.tree_panel: TreePanel = TreePanel(self.notebook, data)
        self.olv_panel: OLVPanel = OLVPanel(self.notebook, data)

        self.notebook.AddPage(self.tree_panel, 'Tree')
        self.notebook.AddPage(self.olv_panel, 'List')

        left_box = wx.BoxSizer(wx.VERTICAL)
        left_box.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(left_box)
