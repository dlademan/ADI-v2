import wx
from pathlib import Path
from Tree import FolderTree

from Data import DataHandler
from Helpers import FileHelpers


class MainFrame(wx.Frame):
    """
    Main frame window of ADI
    """

    def __init__(self, parent, wx_id, title):

        wx.Frame.__init__(self, parent, wx_id, title,
                          pos=wx.DefaultPosition,
                          size=(1100, 800),
                          style=wx.DEFAULT_FRAME_STYLE)

        self.data: DataHandler = DataHandler()
        self.tree_library = None

        self._create_splitter()
        self.set_pos_and_size()

        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.Show()

    def _disable_frame(self, event=None):
        self.main_splitter.Disable()

    def _enable_frame(self, event=None):
        self.main_splitter.Enable()

    def _create_splitter(self):

        sources = self.data.database.select_all_source_folders()
        choices = []
        for source in sources: choices.append(source[1])

        ###################################
        self.main_splitter = wx.SplitterWindow(self)
        self.main_splitter.SetSashGravity(0.5)
        self.main_splitter.SetSashInvisible()

        ###################################
        left_panel = wx.Panel(self.main_splitter)

        self.notebook_library = wx.Notebook(left_panel)

        self.chooser = wx.Choice(left_panel, choices=choices)
        self.chooser.SetSelection(0)
        button_refresh = wx.Button(left_panel, label='Refresh', style=wx.BORDER_NONE)

        font_title = wx.Font(wx.FontInfo(16))
        font_data = wx.Font(wx.FontInfo(11))

        self.count_label = wx.StaticText(left_panel, label='')
        self.size_label = wx.StaticText(left_panel, label='')
        self.count_label.SetFont(font_data)
        self.size_label.SetFont(font_data)

        self.tree_library = FolderTree(left_panel, self.data, self._get_selected_source_path())

        archive_box = wx.BoxSizer()
        archive_box.Add(button_refresh, 0, wx.EXPAND | wx.ALL)
        archive_box.Add(self.chooser, 1, wx.EXPAND | wx.ALL)
        archive_box.Add(0, 0, 2)

        details_box = wx.BoxSizer()
        details_box.Add(10, 0, 0)
        details_box.Add(self.count_label, 0, wx.EXPAND | wx.ALL)
        details_box.Add(20, 0, 0)
        details_box.Add(self.size_label, 0, wx.EXPAND | wx.ALL)

        tree_box = wx.BoxSizer(wx.VERTICAL)
        tree_box.Add(self.tree_library, 1, wx.EXPAND | wx.ALL)

        left_box = wx.BoxSizer(wx.VERTICAL)
        left_box.Add(archive_box, 0, wx.EXPAND | wx.ALL, 5)
        left_box.Add(details_box, 0, wx.EXPAND | wx.ALL, 5)
        left_box.Add(tree_box, 1, wx.EXPAND | wx.ALL, 5)
        left_panel.SetSizer(left_box)

        ###################################
        right_panel = wx.Panel(self.main_splitter)

        ###################################

        self.main_splitter.SplitVertically(left_panel, right_panel)

        # Binds ###########################
        self.chooser.Bind(wx.EVT_CHOICE, self.on_source_change)
        button_refresh.Bind(wx.EVT_BUTTON, self.on_refresh_button_press)

        self._update_source_details()

    def _update_source_details(self):
        source_zip_count = self.tree_library.zip_count
        source_folder_size = FileHelpers.format_bytes(self.tree_library.size)

        zips_text = 'Zips: ' + str(source_zip_count)
        size_text = 'Size: ' + str(source_folder_size)

        self.count_label.SetLabel(zips_text)
        self.size_label.SetLabel(size_text)

    def _get_selected_source_path(self):
        sources = self.data.database.select_all_source_folders()
        selected = self.chooser.GetSelection()
        return Path(sources[selected][1])

    def on_refresh_button_press(self, event=None):
        self._disable_frame()
        self.tree_library.make(self._get_selected_source_path())
        self._update_source_details()
        self._enable_frame()

    def on_source_change(self, event=None):
        pass

    def on_close(self, event=None):
        position = self.GetPosition().Get()
        size = self.GetSize().Get()

        self.data.close(position, size)
        event.Skip()

    def set_pos_and_size(self):
        win_pos = list(self.data.config.win_pos)
        win_pos[0] = int(win_pos[0])
        win_pos[1] = int(win_pos[1])

        win_size = list(self.data.config.win_size)
        win_size[0] = int(win_size[0])
        win_size[1] = int(win_size[1])

        self.SetPosition(wx.Point(*win_pos))
        self.SetSize(wx.Size(*win_size))
