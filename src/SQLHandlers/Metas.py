import logging
from sqlite3 import Error as sqlError

from SQLHandlers.Assets import Assets
from SQLClasses.Meta import Meta


class Metas:

    def __init__(self, connection, assets):
        self.connection = connection
        self.assets: Assets = assets

    def create_meta(self, asset_id: int, product: str, imported: bool = False):
        sql = ''' 
        INSERT INTO metas(asset_id,path,imported) 
        VALUES(?,?,?)
        '''

        meta = (asset_id, product, imported)

        try:
            cursor = self.connection.cursor()
            logging.debug('Inserting \'' + product + '\' into metas table')
            cursor.execute(sql, meta)
            self.connection.commit()
        except sqlError as e:
            logging.critical(e)

    def create_metas_for_all_installed(self):
        assets = self.assets.select_all_assets_by_installed(True)

        # todo create this

    def select_metas_by_imported(self, imported: bool = False):
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM metas WHERE imported=?', (imported,))
            results = cursor.fetchall()
        except sqlError as e:
            logging.critical(e)
            results = []

        metas = []
        for result in results:
            metas.append(Meta(*result))

        return metas

    def update_metas_imported_to(self, asset_id: int, imported: bool):
        asset = self.assets.select_asset_by_id(asset_id)
        sql = ''' 
        UPDATE metas
        SET imported = ?
        WHERE asset_id = ?
        '''

        values = (imported, asset_id)

        try:
            cursor = self.connection.cursor()
            logging.debug('Updating meta import status for ' + asset.product_name)
            cursor.execute(sql, values)
            self.connection.commit()
        except sqlError as e:
            logging.critical(e)