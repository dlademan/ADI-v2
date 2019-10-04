import wx
from pathlib import Path

from MiscWXs.Trees import FolderTree
from Handlers.Data import DataHandler
from Helpers import FileHelpers


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
        self.data = data
        self.titles = []

        font_title = wx.Font(wx.FontInfo(16))
        font_data = wx.Font(wx.FontInfo(11))

        # Create Items ###################
        self.source_choice = wx.Choice(self, choices=self._get_choices(data))
        self.source_choice.SetSelection(0)
        self.button_refresh = wx.Button(self, label='Refresh', style=wx.BORDER_NONE)

        self.count_label = wx.StaticText(self, label='')
        self.size_label = wx.StaticText(self, label='')
        self.count_label.SetFont(font_data)
        self.size_label.SetFont(font_data)

        self.tree: FolderTree = FolderTree(parent=self,
                                           data=data,
                                           source_title=self._get_selected_source_title())

        # Assemble Boxes #################
        archive_box = wx.BoxSizer()
        archive_box.Add(self.button_refresh, 0, wx.EXPAND | wx.ALL)
        archive_box.Add(self.source_choice, 1, wx.EXPAND | wx.ALL)

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

        # Binds ####
        self.button_refresh.Bind(wx.EVT_BUTTON, self.on_refresh_tree)
        self.source_choice.Bind(wx.EVT_CHOICE, self._on_source_change)

    def _get_choices(self, data: DataHandler):
        sources = data.sources.values()
        choices = []

        for source in sources:
            choices.append(str(source.path))
            self.titles.append(source.title)

        return choices

    def _get_selected_source_title(self):
        index = self.source_choice.GetSelection()
        return self.titles[index]

    def on_refresh_tree(self, event=None):
        self._blank_source_details()
        self.tree.make_from_hdd(self._get_selected_source_title())
        self._update_source_details()

    def _on_source_change(self, event=None):
        selection = self.source_choice.GetSelection()
        self.tree.make_from_db(self.titles[selection])

    def _blank_source_details(self):
        self.count_label.SetLabel('')
        self.size_label.SetLabel('')

    def _update_source_details(self):
        source_zip_count = self.tree.zip_count
        source_folder_size = FileHelpers.format_bytes(self.tree.size)

        zips_text = 'Zips: ' + str(source_zip_count)
        size_text = 'Size: ' + str(source_folder_size)

        self.count_label.SetLabel(zips_text)
        self.size_label.SetLabel(size_text)



