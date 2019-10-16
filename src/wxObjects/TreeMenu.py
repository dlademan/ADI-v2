import wx
from pathlib import Path

from Handlers.Data import DataHandler

from sqlObjects.Asset import Asset
from sqlObjects.Folder import Folder
from Helpers import wxHelpers

from Helpers import FileHelpers


class TreeMenu(wx.Menu):

    def __init__(self, data: DataHandler, item_data):
        wx.Menu.__init__(self)

        self.data = data
        self.node_data = item_data

        if item_data['type'] == 'asset':
            self._create_menu_for_asset(item_data['id'])

    def _create_menu_for_asset(self, asset_id):
        asset: Asset = self.data.database.select_asset_by_id(asset_id)
        # todo create a wx.Choice in ui to choose library path
        library_path = Path(self.data.config.libraries['daz_default'])
        args = (asset, library_path)

        if not asset.installed:
            wxHelpers.create_menu_option(self, self, 'Install Asset',
                                         self.data.install_asset, *args)
        elif asset.installed:
            wxHelpers.create_menu_option(self, self, 'Uninstall Asset',
                                         self.data.uninstall_asset, *args)

        wxHelpers.create_menu_option(self, self, 'Open File Location',
                                     FileHelpers.open_location, asset.zip_path)

