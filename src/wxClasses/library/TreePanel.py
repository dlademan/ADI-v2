import wx

from wxClasses.library.Trees import FolderTree
from wxClasses.TreeMenu import TreeMenu
from Handlers.Main import MainHandler
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

    def __init__(self, parent, data: MainHandler):
        wx.Panel.__init__(self, parent=parent)

        self.data = data
        self.source_paths = []

        self._create_widgets()
        self._create_boxes()
        self._bind_widgets()

        self._update_source_details()

    def _create_widgets(self):
        font_data = wx.Font(wx.FontInfo(12))

        # Create Items ###################
        self.source_choice = wx.Choice(self, choices=self._get_choices())
        self.source_choice.SetSelection(0)

        self.button_refresh = wx.Button(self, label='Refresh', style=wx.BORDER_NONE)

        self.count_label = wx.StaticText(self, label='')
        self.size_label = wx.StaticText(self, label='')

        self.count_label.SetFont(font_data)
        self.size_label.SetFont(font_data)

        self.tree: FolderTree = FolderTree(parent=self, data=self.data, source_path=self._get_selected_source_path())

    def _create_boxes(self):
        archive_box = wx.BoxSizer()
        archive_box.Add(self.button_refresh, 0, wx.EXPAND | wx.ALL)
        archive_box.Add(10, 0, 0)
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

    def _bind_widgets(self):
        self.button_refresh.Bind(wx.EVT_BUTTON, self.on_refresh_tree)
        self.source_choice.Bind(wx.EVT_CHOICE, self._on_source_change)
        self.tree.Bind(wx.EVT_TREE_ITEM_MENU, self._on_tree_item_menu)

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

    def _get_choices(self):
        sources = self.data.sources.values()
        choices = []

        for source in sources:
            choices.append(str(source.path))
            self.source_paths.append(source.path)

        return choices

    def _get_selected_source_path(self):
        index: int = self.source_choice.GetSelection()
        return self.source_paths[index]

    def on_refresh_tree(self, event=None):
        self._blank_source_details()
        self.tree.make_from_hdd(self._get_selected_source_path())
        self._update_source_details()

    def _on_source_change(self, event=None):
        selection = self.source_choice.GetSelection()
        self.tree.make_from_db(self.source_paths[selection])
        self._update_source_details()

    def _on_tree_item_menu(self, event=None):
        item_data = self.tree.GetItemData(event.GetItem())
        context_menu = TreeMenu(self.data, item_data)
        self.PopupMenu(context_menu, event.GetPoint())





