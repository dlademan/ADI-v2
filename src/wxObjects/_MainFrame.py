import wx
import logging

from Handlers.Data import DataHandler

from wxObjects.TreePanel import TreePanel
from wxObjects.OLVPanel import OLVPanel
from wxObjects.MenuBar import MenuBar
from wxObjects.DetailsPanel import DetailsPanel

from sqlObjects.Asset import Asset


class MainFrame(wx.Frame):
    """
    Main frame window of ADI

    Attributes:
        self.data:     DataHandler
        self.tree_tab: TreePanel
    """

    def __init__(self, parent, wx_id, title):

        wx.Frame.__init__(self, parent, wx_id, title,
                          pos=wx.DefaultPosition,
                          size=(1100, 800),
                          style=wx.DEFAULT_FRAME_STYLE)

        self.data: DataHandler = DataHandler()
        if self.data.critical:
            logging.critical('ADI Has experienced a critical error during data initialization and must exit')
            return

        self.main_splitter = None
        self.notebook_library = None
        self.tree_panel = None
        self.olv_panel = None

        self._create_body()
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
        self.menu_bar = MenuBar()
        self.SetMenuBar(self.menu_bar)

        self._create_main_splitter()
        self._binds()
        self._set_pos_and_size()

    def _create_main_splitter(self):
        logging.info("Creating main_splitter")

        self.main_splitter = wx.SplitterWindow(self)
        self.main_splitter.SetSashGravity(0.5)
        self.main_splitter.SetSashInvisible()

        left_panel = self._create_left_panel()
        right_panel = self._create_right_panel()

        self.main_splitter.SplitVertically(left_panel, right_panel)

    def _create_left_panel(self):
        left_panel = wx.Panel(self.main_splitter)

        self.notebook_library = wx.Notebook(left_panel)
        self.tree_panel: TreePanel = TreePanel(self.notebook_library, self.data)
        self.olv_panel: OLVPanel = OLVPanel(self.notebook_library, self.data)

        self.notebook_library.AddPage(self.tree_panel, 'Tree')
        self.notebook_library.AddPage(self.olv_panel, 'List')

        left_box = wx.BoxSizer(wx.VERTICAL)
        left_box.Add(self.notebook_library, 1, wx.EXPAND | wx.ALL, 5)
        left_panel.SetSizer(left_box)

        return left_panel

    def _create_right_panel(self):
        self.details_panel = DetailsPanel(self.main_splitter, self.data)

        return self.details_panel

    def _binds(self):
        self.Bind(wx.EVT_CLOSE, self._on_close)
        self.Bind(wx.EVT_MENU, self.tree_panel.on_refresh_tree, self.menu_bar.menus['file_refresh'])
        self.Bind(wx.EVT_MENU, self._on_close, self.menu_bar.menus['file_quit'])
        self.Bind(wx.EVT_MENU, self._on_show_config_frame, self.menu_bar.menus['view_settings'])
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self._on_tree_selection_change, self.tree_panel.tree)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self._on_olv_selection_change, self.olv_panel.olv)

    def _get_selected_source_title(self):
        selection = self.tree_panel.source_choice.GetSelection()
        title = self.tree_panel.titles[selection]
        source = self.data.database.select_source_by_title(title)
        return source

    def _on_show_config_frame(self, event=None):
        logging.debug('Showing config_frame')

    def _on_tree_selection_change(self, event):
        data = self.tree_panel.tree.GetItemData(event.GetItem())

        if data['type'] == 'asset':
            asset = self.data.database.select_asset_by_id(data['id'])
            self.details_panel.update_values_for_asset(asset)
        elif data['type'] == 'folder':
            folder = self.data.database.select_folder_by_id(data['id'])
            self.details_panel.update_values_for_folder(folder)

    def _on_olv_selection_change(self, event=None):
        asset: Asset = self.olv_panel.olv.GetSelectedObject()
        self.details_panel.update_values_for_asset(asset)
