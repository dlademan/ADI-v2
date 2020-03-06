import wx
import logging
from pathlib import Path

from wxClasses.library.Trees import FolderTree
from handlers.Data import DataHandler
from Helpers import FileHelpers


class TestFolderTreeApp(wx.App):
    """Application class for testing FolderTree generation"""

    def OnInit(self):
        frame = TestFolderTreeFrame(None, "TestFolderTreeFrame")

        return True


class TestFolderTreeFrame(wx.Frame):

    def __init__(self, parent, title):

        wx.Frame.__init__(self, parent, wx.ID_ANY, title,
                          pos=wx.DefaultPosition,
                          size=(600, 800),
                          style=wx.DEFAULT_FRAME_STYLE)

        self.library_panel = None
        self.chooser = None
        self.tree = None

        self.data = DataHandler()
        self.set_pos_and_size()

        self.data.db.create_folder(Path(r'D:\Files\DAZ Zips'), True)
        self.data.db.create_folder(Path(r'D:\Files\DAZ Archive'), True)

        self._create_body()
        self.Show()
        logging.info('---------------- TestFolderTree Shown')

        self.Bind(wx.EVT_CLOSE, self.on_close)

    def _disable_frame(self, event=None):
        self.library_panel.Disable()

    def _enable_frame(self, event=None):
        self.library_panel.Enable()

    def _get_selected_source_path(self):
        sources = self.data.db.select_all_sources()
        selected = self.chooser.GetSelection()
        return Path(sources[selected][1])

    def _create_body(self):
        # data to be used to create stuff
        font_title = wx.Font(wx.FontInfo(16))
        font_data = wx.Font(wx.FontInfo(11))

        sources = self.data.db.select_all_sources()
        choices = []
        for source in sources:
            choices.append(source[1])

        # creation of widgets
        self.library_panel = wx.Panel(self)
        main_box = wx.BoxSizer(wx.VERTICAL)

        self.chooser = wx.Choice(self.library_panel, choices=choices)
        self.chooser.SetSelection(0)
        button_refresh = wx.Button(self.library_panel, label='Refresh', style=wx.BORDER_NONE)

        archive_box = wx.BoxSizer()
        archive_box.Add(button_refresh, 0, wx.EXPAND | wx.ALL)
        archive_box.Add(self.chooser, 1, wx.EXPAND | wx.ALL)
        archive_box.Add(0, 0, 2)

        self.count_label = wx.StaticText(self.library_panel, label='')
        self.size_label = wx.StaticText(self.library_panel, label='')
        self.count_label.SetFont(font_data)
        self.size_label.SetFont(font_data)

        details_box = wx.BoxSizer()
        details_box.Add(10, 0, 0)
        details_box.Add(self.count_label, 0, wx.EXPAND | wx.ALL)
        details_box.Add(20, 0, 0)
        details_box.Add(self.size_label, 0, wx.EXPAND | wx.ALL)

        tree_box = wx.BoxSizer(wx.VERTICAL)
        self.tree = FolderTree(self.library_panel, self.data.db, Path(sources[0][1]))
        tree_box.Add(self.tree, wx.ID_ANY, wx.EXPAND | wx.ALL)

        main_box.Add(archive_box, 0, wx.EXPAND | wx.ALL, 5)
        main_box.Add(details_box, 0, wx.EXPAND | wx.ALL, 5)
        main_box.Add(tree_box, wx.ID_ANY, wx.EXPAND | wx.ALL, 5)
        self.library_panel.SetSizer(main_box)

        self.chooser.Bind(wx.EVT_CHOICE, self.on_source_change)
        button_refresh.Bind(wx.EVT_BUTTON, self.on_refresh_button_press)

        self._update_source_details()

    def _update_source_details(self):
        source_zip_count = self.tree.zip_count
        source_folder_size = FileHelpers.format_bytes(self.tree.size)

        zips_text = 'Zips: ' + str(source_zip_count)
        size_text = 'Size: ' + str(source_folder_size)

        self.count_label.SetLabel(zips_text)
        self.size_label.SetLabel(size_text)

    def on_refresh_button_press(self, event=None):
        self._disable_frame()
        self.tree.make_from_hdd(self._get_selected_source_path())
        self._update_source_details()
        self._enable_frame()

    def on_source_change(self, event=None):
        pass

    def on_close(self, event=None):
        logging.debug('on_close')
        position = self.GetPosition().Get()
        size = self.GetSize().Get()

        self.data.close(position, size)
        event.Skip()

    def set_pos_and_size(self):
        self.SetPosition(self.data.config.win_pos)
        self.SetSize(self.data.config.win_size)


app = TestFolderTreeApp()
app.MainLoop()
