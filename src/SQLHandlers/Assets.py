import logging
from pathlib import Path
from sqlite3 import Error as sqlError

from Helpers import FileHelpers
from SQLClasses.Asset import Asset


class Assets:

    def __init__(self, connection):
        self.connection = connection

    def create_asset(self, path: Path, source_id: int):

        if path.suffix != '.zip':
            logging.critical('Path provided does not point to a zip file')
            return None

        found, asset = self.select_asset_by_zip(path)
        if found: return asset

        logging.debug('Creating asset from: ' + path.name)

        sku = FileHelpers.get_sku(path)
        product_name = FileHelpers.get_product_name(path)
        path_str = str(path.parent)
        filename = path.name
        zip_size = FileHelpers.get_file_size(path)
        installed = False  # todo check if asset is already installed

        asset = (source_id, sku, product_name, path_str, filename, zip_size, installed)

        sql = ''' 
        INSERT INTO assets(source_id,sku,product_name,path,filename,zip_size,installed) 
        VALUES(?,?,?,?,?,?,?)
        '''

        cursor = self.connection.cursor()
        try:
            logging.debug('Inserting ' + asset[4] + ' into assets table')
            cursor.execute(sql, asset)
            self.connection.commit()
        except sqlError as e:
            logging.critical(e)

        return Asset(cursor.lastrowid, *asset)

    def select_all_assets(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM assets')
        rows = cursor.fetchall()
        assets = []
        for row in rows:
            assets.append(Asset(*row))

        return assets

    def select_all_assets_by_installed(self, installed: bool):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM assets WHERE installed=?', (installed,))
        results = cursor.fetchall()
        assets = []
        for row in results:
            assets.append(Asset(*row))

        return assets

    def select_asset_by_id(self, asset_id: int):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM assets WHERE id=?', (asset_id,))
        return Asset(*cursor.fetchone())

    def select_asset_by_zip(self, path: Path):
        logging.debug('Trying to find asset in database from: ' + path.name)

        if path.suffix != '.zip':
            logging.critical('Path provided does not point to a zip file,')
            return False, None

        # todo add select by date_created
        path_size = FileHelpers.get_file_size(path)
        success, asset = self.select_asset_by_size_and_filename(path_size, path.name)

        if success:
            logging.debug('Found: ' + path.name)
            return True, asset
        else:
            logging.debug('Not Found: ' + path.name)
            return False, None

    def select_all_assets_by_source_id(self, source_id: int):
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM assets WHERE source_id=?', (source_id,))
            rows = cursor.fetchall()
        except sqlError as e:
            logging.critical(e)
            return None

        assets = []
        for row in rows:
            assets.append(Asset(*row))

        return assets

    def select_asset_by_size_and_filename(self, size: int, name: str):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM assets WHERE zip_size=? AND filename=?', (size, name))
        result = cursor.fetchone()

        if result is None:
            success = False
            asset = result
        else:
            success = True
            asset = Asset(*result)

        return success, asset

    def update_asset_installed(self, installed: bool, asset_id: int = None):
        asset = self.select_asset_by_id(asset_id)
        sql = ''' 
        UPDATE assets
        SET installed = ?
        WHERE id = ?
        '''

        values = (installed, asset_id)

        try:
            cursor = self.connection.cursor()
            logging.debug('Asset: ' + asset.product_name)
            logging.debug('Updating installed to: ' + str(installed))
            cursor.execute(sql, values)
            self.connection.commit()
        except sqlError as e:
            logging.critical(e)