import logging
import wx
from pathlib import Path

from Handlers.Main import MainHandler
from Helpers import FileHelpers
from SQLClasses.Folder import Folder
from SQLClasses.Source import Source
from SQLClasses.Asset import Asset


class FolderTree(wx.TreeCtrl):

    def __init__(self, parent, data: MainHandler, source_path: Path,
                 wx_id=wx.ID_ANY, position=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):

        wx.TreeCtrl.__init__(self, parent, wx_id, position, size, style)

        self.root_node = None
        self.data = data
        self.zip_count = 0
        self.size = 0

        self.AssignImageList(self.create_image_list())

        self.make_from_hdd(source_path)

    def make_from_hdd(self, source_path: Path):
        self.DeleteAllItems()
        self.zip_count = 0
        self.size = 0

        source: Source = self.data.sql_handler.sources.select_source_by_path(str(source_path))

        logging.info("Making tree by path with: " + str(source.path.name))
        root_data = {'id': source.id_,
                     'type': 'folder',
                     'path': source.path}

        self.root_node = self.AddRoot(source.path.name, data=root_data)
        node_list = self.populate(self.root_node, root_data, source.id_)

        for node in node_list:
            if self.GetItemData(node)['type'] == 'folder' and self.GetChildrenCount(node) < 1:
                self.Delete(node)

        logging.info("Finished making tree")

    def populate(self, current_node, current_data, source_id: int):
        node_list = []

        sub_list = [x for x in current_data['path'].iterdir()]

        for sub_path in sub_list:

            if sub_path.is_dir():
                folder: Folder = self.data.sql_handler.folders.create_folder(sub_path, source_id)
                next_data = {'id': folder.id_,
                             'type': 'folder',
                             'path': folder.path}

                next_node = self.AppendItem(current_node, sub_path.name, data=next_data, image=0)
                node_list.append(next_node)

                temp_list = self.populate(next_node, next_data, source_id)
                node_list += temp_list

            elif sub_path.suffix == '.zip':
                self.zip_count += 1
                self.size += FileHelpers.get_file_size(sub_path)

                asset: Asset = self.data.sql_handler.assets.create_asset(sub_path, source_id)
                next_data = {'id': asset.id_,
                             'type': 'asset',
                             'path': sub_path}

                next_node = self.AppendItem(current_node, asset.product_name, data=next_data, image=1)
                node_list.append(next_node)

        self.SortChildren(current_node)
        return node_list

    def make_from_db(self, source_path: Path):
        self.DeleteAllItems()
        self.zip_count = 0
        self.size = 0
        node_list = {}

        source: Source = self.data.sql_handler.sources.select_source_by_path(str(source_path))
        logging.info('Making tree from database with source: ' + str(source.path))

        folders = self.data.sql_handler.folders.select_all_folders_by_source_id(source.id_)
        if folders is None or len(folders) < 1:
            logging.error('SQL could not find any folders from source_id_: ' + str(source.id_))
            return

        root_data = {'id': source.id_,
                     'type': 'folder',
                     'path': source.path}

        node_list[str(source.path)] = self.root_node = self.AddRoot(source.path.name, data=root_data)

        for folder in folders:
            folder = Folder(*folder)

            parent_key = str(folder.path.parent)
            parent_node = node_list[parent_key]
            folder_data = {'id': folder.id_,
                           'type': 'folder',
                           'path': folder.path}

            node_list[str(folder.path)] = self.AppendItem(parent_node, folder.title, data=folder_data, image=0)

        assets = self.data.sql_handler.assets.select_all_assets_by_source_id(source.id_)

        for asset in assets:
            self.zip_count += 1
            self.size += asset.size_raw

            parent_key = str(asset.path)
            parent_node = node_list[parent_key]
            asset_data = {'id': asset.id_,
                          'type': 'asset',
                          'path': asset.path}

            asset_key = str(asset.path) + str(asset.filename)

            node_list[asset_key] = self.AppendItem(parent_node, asset.product_name, data=asset_data, image=1)

        for node in node_list.values():
            if self.GetItemData(node)['type'] == 'folder' and self.GetChildrenCount(node) < 1:
                self.Delete(node)

        logging.info("Finished making tree")

    def OnCompareItems(self, item1, item2):
        text1 = self.GetItemText(item1)
        text2 = self.GetItemText(item2)
        is_dir1 = self.GetItemData(item1)['path'].is_dir()
        is_dir2 = self.GetItemData(item2)['path'].is_dir()

        if (is_dir1 and is_dir2) and text1 < text2:
            return -1
        elif (is_dir1 and is_dir2) and text1 == text2:
            return 0
        elif is_dir1 and is_dir2:
            return 1
        elif is_dir1 and not is_dir2:
            return -1
        elif not is_dir1 and is_dir2:
            return 1
        elif text1 < text2:
            return -1
        elif text1 == text2:
            return 0
        else:
            return 1

    @staticmethod
    def create_image_list():
        image_list = wx.ImageList(18, 18)

        bitmap_directory = wx.Bitmap('tests/0_directory_18.png', wx.BITMAP_TYPE_ANY)
        bitmap_zip = wx.Bitmap('tests/1_zip_18.png', wx.BITMAP_TYPE_ANY)

        image_list.Add(bitmap_directory)
        image_list.Add(bitmap_zip)

        return image_list
