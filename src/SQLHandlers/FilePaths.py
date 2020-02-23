import logging
from pathlib import Path
from sqlite3 import Error as sqlError
from zipfile import ZipFile, BadZipFile

from SQLHandlers.Assets import Assets
from Helpers import FileHelpers


class FilePaths:

    def __init__(self, connection, assets):
        self.connection = connection
        self.assets: Assets = assets

    def create_all_file_paths(self, asset_ids: list):
        for asset_id in asset_ids:
            self.create_all_file_paths_for_asset_id(asset_id)

    def create_all_file_paths_for_asset_id(self, asset_id: int):
        results = self.select_file_paths_by_id(asset_id)
        asset = self.assets.select_asset_by_id(asset_id)

        asset_path = Path(asset.path) / Path(asset.filename)

        try:
            with ZipFile(asset_path) as asset_zip_file:
                info_list = asset_zip_file.infolist()
        except BadZipFile as e:
            logging.error('Error occurred while opening zip file: ' + str(asset_path.name))
            logging.error(e)
            logging.info('File paths not created for: ' + str(asset_path.name))
            return

        file_paths = []
        for info in info_list:
            if not info.is_dir():
                file_path = (asset_id, FileHelpers.clean_path(info.filename))
                file_paths.append(file_path)

        if len(results) == len(file_paths): return

        try:
            logging.debug('Creating file_path for: ' + asset_path.name)
            cursor = self.connection.cursor()
            cursor.executemany('INSERT INTO file_paths VALUES(?,?);', file_paths)
            self.connection.commit()
        except sqlError as e:
            logging.critical(e)

    def create_single_file_path_for_asset_id(self, asset_id: int, file_path: Path):
        value = (asset_id, str(file_path))

        try:
            logging.debug('Creating file_path: ' + str(asset_id) + ', ' + str(file_path))
            cursor = self.connection.cursor()
            cursor.execute('INSERT INTO file_paths VALUES(?,?);', value)
            self.connection.commit()
        except sqlError as e:
            logging.critical(e)

    def select_file_paths_by_id(self, asset_id: int):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM file_paths WHERE asset_id=?', (asset_id,))
        results = cursor.fetchall()
        return results