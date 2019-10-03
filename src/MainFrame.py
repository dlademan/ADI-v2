import wx
import logging
from pathlib import Path

from Data import DataHandler
from Helpers import FileHelpers
from TreePanel import TreePanel
from MenuBar import MenuBar


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
        self.tree_tab: TreePanel = None

        # todo get rid of this hack
        # create a proper config window and prompt on start
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
        self.menu_bar = MenuBar()

        self.SetMenuBar(self.menu_bar)

    def _create_main_splitter(self):
        logging.info("Creating main_splitter")

        self.main_splitter = wx.SplitterWindow(self)
        self.main_splitter.SetSashGravity(0.5)
        self.main_splitter.SetSashInvisible()

        left_panel = self._create_left_panel()
        right_panel = self._create_right_panel()

        self.main_splitter.SplitVertically(left_panel, right_panel)
        self._update_source_details()

        # Binds #########################
        self.tree_tab.chooser.Bind(wx.EVT_CHOICE, self._on_source_change)
        self.tree_tab.button_refresh.Bind(wx.EVT_BUTTON, self._on_refresh_tree)

        self.Bind(wx.EVT_MENU, self._on_refresh_tree, self.menu_bar.menus['file_refresh'])
        self.Bind(wx.EVT_MENU, self._on_close, self.menu_bar.menus['file_quit'])
        self.Bind(wx.EVT_MENU, self._on_show_config_frame, self.menu_bar.menus['view_settings'])

    def _create_left_panel(self):
        left_panel = wx.Panel(self.main_splitter)

        self.notebook_library = wx.Notebook(left_panel)
        self.tree_tab: TreePanel = TreePanel(self.notebook_library, self.data)
        self.notebook_library.AddPage(self.tree_tab, 'Tree')

        left_box = wx.BoxSizer(wx.VERTICAL)
        left_box.Add(self.notebook_library, 1, wx.EXPAND | wx.ALL, 5)
        left_panel.SetSizer(left_box)

        return left_panel

    def _create_right_panel(self):
        right_panel = wx.Panel(self.main_splitter)

        return right_panel

    def _update_source_details(self):
        source_zip_count = self.tree_tab.tree.zip_count
        source_folder_size = FileHelpers.format_bytes(self.tree_tab.tree.size)

        zips_text = 'Zips: ' + str(source_zip_count)
        size_text = 'Size: ' + str(source_folder_size)

        self.tree_tab.count_label.SetLabel(zips_text)
        self.tree_tab.size_label.SetLabel(size_text)

    def _blank_source_details(self):
        self.tree_tab.count_label.SetLabel('')
        self.tree_tab.size_label.SetLabel('')

    def _get_selected_source_path(self):
        sources = self.data.database.select_all_source_folders()
        selected = self.tree_tab.chooser.GetSelection()
        return Path(sources[selected][3])

    def _on_refresh_tree(self, event=None):
        self._disable_frame()
        self._blank_source_details()
        self.tree_tab.tree.make_from_path(self._get_selected_source_path(), self.tree_tab.chooser.GetSelection())
        self._update_source_details()
        self._enable_frame()

    def _on_source_change(self, event=None):
        self._disable_frame()
        self._blank_source_details()

        self.tree_tab.tree.make_from_db(self.tree_tab.chooser.GetSelection())

        self._update_source_details()
        self._enable_frame()

    def _on_show_config_frame(self, event=None):
        logging.debug('Showing config_frame')
