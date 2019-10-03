import wx
import logging
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

        self.data.database.create_folder(Path(r'D:\Files\DAZ Zips'), 0, True)
        self.data.database.create_folder(Path(r'D:\Files\DAZ Archive'), 1, True)

        self._create_body()

        self.Bind(wx.EVT_CLOSE, self._on_close)

        self.Show()

    def _enable_frame(self, event=None):
        self.main_splitter.Enable()

    def _disable_frame(self, event=None):
        self.main_splitter.Disable()

    def _on_close(self, event=None):
        self.data.close(self.GetPosition().Get(),
                        self.GetSize().Get())
        event.Skip()
        self.Destroy()

    def _set_pos_and_size(self):
        self.SetPosition(wx.Point(*self.data.config.win_pos))
        self.SetSize(wx.Size(*self.data.config.win_size))

    def _create_body(self):
        self._create_menu_bar()
        self._create_main_splitter()
        self._set_pos_and_size()

    def _create_menu_bar(self):
        logging.info("Creating menu_bar")

        ##### File Menu #################
        file_menu = wx.Menu()
        file_refresh = wx.MenuItem(file_menu, -1, '&Refresh')
        file_quit = wx.MenuItem(file_menu, wx.ID_EXIT, '&Quit')

        self.Bind(wx.EVT_MENU, self._on_refresh_tree, file_refresh)
        self.Bind(wx.EVT_MENU, self._on_close, file_quit)

        file_menu.Append(file_refresh)
        file_menu.AppendSeparator()
        file_menu.Append(file_quit)

        ##### Library Menu ###############

        ##### View Menu ##################
        view_menu = wx.Menu()
        view_settings = wx.MenuItem(view_menu, wx.ID_ANY, '&Configuration')

        self.Bind(wx.EVT_MENU, self._on_show_config_frame, view_settings)

        view_menu.Append(view_settings)

        ##### Menu Bar ###################

        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, '&File')
        # menu_bar.Append(lib_menu, '&Library')
        menu_bar.Append(view_menu, '&View')
        self.SetMenuBar(menu_bar)

        pass

    def _create_main_splitter(self):
        logging.info("Creating main_splitter")

        sources = self.data.database.select_all_source_folders()
        choices = []
        for source in sources: choices.append(source[4])

        ###################################
        self.main_splitter = wx.SplitterWindow(self)
        self.main_splitter.SetSashGravity(0.5)
        self.main_splitter.SetSashInvisible()

        ###################################
        left_panel = wx.Panel(self.main_splitter)

        self.notebook_library = wx.Notebook(left_panel)

        self.chooser = wx.Choice(left_panel, choices=choices)
        self.chooser.SetSelection(0)
        # if len(choices) < 2: self.chooser.Disable()
        button_refresh = wx.Button(left_panel, label='Refresh', style=wx.BORDER_NONE)

        font_title = wx.Font(wx.FontInfo(16))
        font_data = wx.Font(wx.FontInfo(11))

        self.count_label = wx.StaticText(left_panel, label='')
        self.size_label = wx.StaticText(left_panel, label='')
        self.count_label.SetFont(font_data)
        self.size_label.SetFont(font_data)

        self.tree_library = FolderTree(parent=left_panel,
                                       data=self.data,
                                       root_path=self._get_selected_source_path(),
                                       source_index=self.chooser.GetSelection())

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
        self.chooser.Bind(wx.EVT_CHOICE, self._on_source_change)
        button_refresh.Bind(wx.EVT_BUTTON, self._on_refresh_tree)

        self._update_source_details()

    def _update_source_details(self):
        source_zip_count = self.tree_library.zip_count
        source_folder_size = FileHelpers.format_bytes(self.tree_library.size)

        zips_text = 'Zips: ' + str(source_zip_count)
        size_text = 'Size: ' + str(source_folder_size)

        self.count_label.SetLabel(zips_text)
        self.size_label.SetLabel(size_text)

    def _blank_source_details(self):
        self.count_label.SetLabel('Zips:')
        self.size_label.SetLabel('Size:')

    def _get_selected_source_path(self):
        sources = self.data.database.select_all_source_folders()
        selected = self.chooser.GetSelection()
        return Path(sources[selected][3])

    def _on_refresh_tree(self, event=None):
        self._disable_frame()
        self._blank_source_details()
        self.tree_library.make(self._get_selected_source_path(), self.chooser.GetSelection())
        self._update_source_details()
        self._enable_frame()

    def _on_source_change(self, event=None):
        self._on_refresh_tree()

    def _on_show_config_frame(self, event=None):
        logging.debug('Showing config_frame')
