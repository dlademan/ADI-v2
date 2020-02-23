import wx
from pathlib import Path

from Handlers.Main import MainHandler

from SQLClasses.Asset import Asset
from SQLClasses.Folder import Folder
from Helpers import WXHelpers

from Helpers import FileHelpers


class TreeMenu(wx.Menu):

    def __init__(self, data: MainHandler, item_data):
        wx.Menu.__init__(self)

        self.data = data
        self.node_data = item_data

        if item_data['type'] == 'asset':
            self._create_menu_for_asset(item_data['id'])
        elif item_data['type'] == 'folder':
            self._create_menu_for_folder(item_data['id'])

    def _create_menu_for_asset(self, asset_id):
        asset: Asset = self.data.sql_handler.assets.select_asset_by_id(asset_id)
        # todo create a wx.Choice in ui to choose library path
        library_path = Path(self.data.config.libraries['daz_default'])
        args = (asset, library_path)

        if not asset.installed:
            WXHelpers.create_menu_option(self, self, 'Install Asset',
                                         self.data.install_asset, *args)
        elif asset.installed:
            WXHelpers.create_menu_option(self, self, 'Uninstall Asset',
                                         self.data.uninstall_asset, *args)

        WXHelpers.create_menu_option(self, self, 'Open File Location',
                                     FileHelpers.open_location, asset.zip_path)

    def _create_menu_for_folder(self, folder_id):
        folder: Folder = self.data.sql_handler.folders.select_folder_by_id(folder_id)

        WXHelpers.create_menu_option(self, self, 'Open Folder Location',
                                     FileHelpers.open_location, folder.path)

