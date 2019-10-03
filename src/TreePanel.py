import wx
from pathlib import Path

from Trees import FolderTree
from Data import DataHandler


class TreePanel(wx.Panel):
    """
    Panel that contains the tree view of a library

    Attributes:
        self.chooser:        wx.Choice
        self.button_refresh: wx.Button
        self.count_label:    wx.StaticText
        self.size_label:     wx.StaticText
        self.tree:           FolderTree: wx.TreeCtrl

    """

    def __init__(self, parent, data: DataHandler):
        wx.Panel.__init__(self, parent=parent)

        # Values to be used ##############
        sources = data.database.select_all_source_folders()
        choices = []
        for source in sources: choices.append(source[3])

        font_title = wx.Font(wx.FontInfo(16))
        font_data = wx.Font(wx.FontInfo(11))

        # Create Items ###################
        self.chooser = wx.Choice(self, choices=choices)
        self.chooser.SetSelection(0)
        self.button_refresh = wx.Button(self, label='Refresh', style=wx.BORDER_NONE)

        self.count_label = wx.StaticText(self, label='')
        self.size_label = wx.StaticText(self, label='')
        self.count_label.SetFont(font_data)
        self.size_label.SetFont(font_data)

        self.tree: FolderTree = FolderTree(parent=self,
                                           data=data,
                                           root_path=self._get_selected_source_path(data),
                                           source_index=self.chooser.GetSelection())

        # Assemble Boxes #################
        archive_box = wx.BoxSizer()
        archive_box.Add(self.button_refresh, 0, wx.EXPAND | wx.ALL)
        archive_box.Add(self.chooser, 1, wx.EXPAND | wx.ALL)
        archive_box.Add(0, 0, 2)

        details_box = wx.BoxSizer()
        details_box.Add(10, 0, 0)
        details_box.Add(self.count_label, 0, wx.EXPAND | wx.ALL)
        details_box.Add(20, 0, 0)
        details_box.Add(self.size_label, 0, wx.EXPAND | wx.ALL)

        tree_box = wx.BoxSizer(wx.VERTICAL)
        tree_box.Add(self.tree, 1, wx.EXPAND | wx.ALL)

        main_box = wx.BoxSizer(wx.VERTICAL)
        main_box.Add(archive_box, 0, wx.EXPAND | wx.ALL, 5)
        main_box.Add(details_box, 0, wx.EXPAND | wx.ALL, 5)
        main_box.Add(tree_box, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(main_box)

    def _get_selected_source_path(self, data: DataHandler):
        sources = data.database.select_all_source_folders()
        selected = self.chooser.GetSelection()
        return Path(sources[selected][3])


