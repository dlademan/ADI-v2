import wx
import logging

from Handlers.Data import DataHandler

from wxObjects.TreePanel import TreePanel
from wxObjects.OLVPanel import OLVPanel
from wxObjects.MenuBar import MenuBar
from wxObjects.DetailsPanel import DetailsPanel
from wxObjects.NotebookPanel import NotebookPanel

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

        logging.info('------------------- ADI Started')

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
        self.data.close(position=self.GetPosition().Get(),
                        size=self.GetSize().Get())
        event.Skip()
        logging.info('-------------------- ADI Closed')
        self.Destroy()

    def _set_pos_and_size(self):
        self.SetPosition(wx.Point(*self.data.config.win_pos))
        self.SetSize(wx.Size(*self.data.config.win_size))

    def _create_body(self):
        logging.debug('Creating ADI main frame')
        self.menu_bar = MenuBar()
        self.SetMenuBar(self.menu_bar)
        self._create_main_splitter()
        logging.debug('Finished ADI main frame')

        self._binds()
        self._set_pos_and_size()

    def _create_main_splitter(self):
        logging.debug("Creating main_splitter")

        self.main_splitter = wx.SplitterWindow(self)
        self.main_splitter.SetSashGravity(0.5)

        self.notebook_panel: NotebookPanel = NotebookPanel(self.main_splitter, self.data)
        self.details_panel: DetailsPanel = DetailsPanel(self.main_splitter, self.data)

        self.main_splitter.SplitVertically(self.notebook_panel, self.details_panel)
        logging.debug("Finished main_splitter")

    def _binds(self):
        # Main Frame Binds #############
        self.Bind(wx.EVT_CLOSE, self._on_close)

        # Menu Bar Binds ###############
        self.Bind(wx.EVT_MENU, self.notebook_panel.tree_panel.on_refresh_tree, self.menu_bar.menus['file_refresh'])
        self.Bind(wx.EVT_MENU, self._on_close, self.menu_bar.menus['file_quit'])

        self.Bind(wx.EVT_MENU, self._on_import_meta, self.menu_bar.menus['library_import_meta'])

        self.Bind(wx.EVT_MENU, self._on_show_config_frame, self.menu_bar.menus['view_settings'])

        # Tree Binds ###################
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self._on_tree_selection_change, self.notebook_panel.tree_panel.tree)

        # OLV Binds ####################
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self._on_olv_selection_change, self.notebook_panel.olv_panel.olv)

    def _get_selected_source_title(self):
        selection = self.tree_panel.source_choice.GetSelection()
        title = self.tree_panel.titles[selection]
        source = self.data.database.select_source_by_title(title)
        return source

    def _on_show_config_frame(self, event=None):
        logging.debug('Showing config_frame')

    def _on_import_meta(self, event=None):
        metas = self.data.database.select_metas_by_imported(False)

        self.data.write_meta_import_script(metas)
        self.data.execute_meta_import_script()

        for meta in metas:
            self.data.database.update_metas_imported_to(meta.asset_id, True)

    def _on_tree_selection_change(self, event):
        data = self.notebook_panel.tree_panel.tree.GetItemData(event.GetItem())

        if data['type'] == 'asset':
            asset = self.data.database.select_asset_by_id(data['id'])
            self.details_panel.update_values_for_asset(asset)
        elif data['type'] == 'folder':
            folder = self.data.database.select_folder_by_id(data['id'])
            self.details_panel.update_values_for_folder(folder)

    def _on_olv_selection_change(self, event=None):
        asset: Asset = self.notebook_panel.olv_panel.olv.GetSelectedObject()
        self.details_panel.update_values_for_asset(asset)
