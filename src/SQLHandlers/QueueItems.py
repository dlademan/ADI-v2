import logging
from sqlite3 import Error as sqlError

from SQLHandlers.Assets import Assets
from SQLClasses.QueueItem import QueueItem


class QueueItems:

    def __init__(self, connection, assets):
        self.connection = connection
        self.assets: Assets = assets

    def create_queue_item(self, asset_id: int, process: int):
        asset = self.assets.select_asset_by_id(asset_id)

        sql = ''' 
        INSERT INTO queue_items(asset_id,process,status,pos) 
        VALUES(?,?,?,?)
        '''
        process_text = 'installed' if process == 0 else 'uninstalled'
        status = False
        pos = self.get_queue_length()

        queue_item = (asset_id, process, status, pos)

        try:
            cursor = self.connection.cursor()
            logging.debug('Inserting \'' + asset.product_name + '\' into queue to be' + process_text)
            cursor.execute(sql, queue_item)
            self.connection.commit()
        except sqlError as e:
            logging.critical(e)

    def select_all_queue_items(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM queue_items')
            results = cursor.fetchall()
        except sqlError as e:
            logging.critical(e)
            return None

        queue_items = []
        for result in results:
            queue_items.append(QueueItem(*result))

        return queue_items

    def get_queue_length(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM queue_items')
            results = cursor.fetchall()
            return len(results)
        except sqlError as e:
            logging.critical(e)
            return None
