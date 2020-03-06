import wx
from pathlib import Path

from handlers.Data import DataHandler

from sql.DBClasses import Asset, Folder
from Helpers import WXHelpers

from Helpers import FileHelpers


class TreeMenu(wx.Menu):

    def __init__(self, data: DataHandler, item_data):
        wx.Menu.__init__(self)

        self.data = data
        self.node_data = item_data

        if item_data['type'] == 'asset':
            self._create_menu_for_asset(item_data['id'])
        elif item_data['type'] == 'folder':
            self._create_menu_for_folder(item_data['id'])

    def _create_menu_for_asset(self, asset_id):
        asset: Asset = self.data.db.assets[asset_id]
        # todo create a wx.Choice in ui to choose library path
        library_path = Path(self.data.config.libraries['library_1'])

        if not asset.installed_raw:
            WXHelpers.create_menu_option(self, self, 'Install Asset',
                                         self.data.install_asset, asset, library_path)

            WXHelpers.create_menu_option(self, self, 'Queue to be Installed',
                                         self.data.db.queue.create, asset_id, 0, 0)
        elif asset.installed_raw:
            WXHelpers.create_menu_option(self, self, 'Uninstall Asset',
                                         self.data.uninstall_asset, asset, library_path)

            WXHelpers.create_menu_option(self, self, 'Queue to be Uninstalled',
                                         self.data.db.queue.create, asset_id, 0, 1)

        WXHelpers.create_menu_option(self, self, 'Open File Location',
                                     FileHelpers.open_location, asset.path)

    def _create_menu_for_folder(self, folder_id):
        folder: Folder = self.data.db.folders[folder_id]

        WXHelpers.create_menu_option(self, self, 'Open Folder Location',
                                     FileHelpers.open_location, folder.path)

