import logging
import sqlite3
from sqlite3 import Error as sqlError
from pathlib import Path
from zipfile import ZipFile, BadZipFile

from Helpers import FileHelpers, FolderHelpers
from sqlObjects.Asset import Asset
from sqlObjects.Folder import Folder
from sqlObjects.Source import Source


class DatabaseHandler:

    def __init__(self, filename: str = 'assets.db'):
        self.filename: str = filename
        self.path: Path = FolderHelpers.get_user_folder() / filename

        self.connection = self._init_connection()
        self._init_tables()

        if self.connection is not None:
            self.connection.commit()

    def _init_connection(self):

        connection = None
        try:
            connection = sqlite3.connect(str(self.path))
            logging.info("Connection created to " + self.filename)
            logging.debug("SQLite version: " + sqlite3.version)
        except sqlError as e:
            logging.critical(e)

        return connection

    def _init_table(self, table_name, sql_table):
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql_table)
        except sqlError as e:
            logging.critical(table_name + ": ")
            logging.critical(e)

    def _init_tables(self):
        tables = []

        with open(r'src\tables', 'r') as tables_file:
            for line in tables_file:
                if line[:12] == 'CREATE TABLE':
                    tables.append('')
                    tables[-1] += line
                    continue
                elif line == '\n': continue
                else: tables[-1] += line

        if self.connection is not None:
            for i, table in enumerate(tables):
                self._init_table("Table " + str(i), table)
        else:
            logging.critical("Error! Cannot create the database connection.")

    def create_asset(self, path: Path, source_id: int):

        if path.suffix != '.zip':
            logging.critical('Path provided does not point to a zip file')
            return None

        found, asset = self.find_asset_by_zip(path)
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

    def select_asset_by_id(self, asset_id: int):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM assets WHERE id=?', (asset_id,))
        return Asset(*cursor.fetchone())

    def find_asset_by_zip(self, path: Path):
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

    def select_all_assets(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM assets')
        rows = cursor.fetchall()
        assets = []
        for row in rows:
            assets.append(Asset(*row))

        return assets

    def select_asset_by_size(self, size: int):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM assets WHERE zip_size=?', (size,))
        rows = cursor.fetchall()

        if len(rows) > 0:
            return True, rows
        else:
            return False, None

    def select_asset_by_filename(self, name: str):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM assets WHERE filename=?', (name,))
        rows = cursor.fetchall()

        if len(rows) > 0:
            return True, rows
        else:
            return False, None

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

    def create_folder(self, path: Path, source_id: int):

        folder = self.select_folder_by_path(path)
        if isinstance(folder, Folder): return folder

        sql = ''' 
        INSERT INTO folders(source_id,path,title,file_count,size_raw) 
        VALUES(?,?,?,?,?)
        '''

        title = path.name
        file_count = FolderHelpers.get_zip_count(path)
        size_raw = FolderHelpers.get_folder_size(path)

        folder = (source_id, str(path), title, file_count, size_raw)

        try:
            cursor = self.connection.cursor()
            logging.debug('Inserting \'' + path.name + '\' into folders table')
            cursor.execute(sql, folder)
            self.connection.commit()
            return Folder(cursor.lastrowid, *folder)
        except sqlError as e:
            logging.critical(e)
            return None

    def select_folder_by_path(self, path: Path):
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM folders WHERE path=?', (str(path),))
            result = cursor.fetchone()
        except sqlError as e:
            logging.critical(e)
            return None

        if result is not None:
            return Folder(*result)
        else:
            return None

    def select_folder_by_id(self, folder_id: int):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM folders WHERE id=?', (folder_id,))
        return Folder(*cursor.fetchone())

    def select_all_folders_by_source_id(self, source_id: int):
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM folders WHERE source_id=?', (source_id,))
            return cursor.fetchall()
        except sqlError as e:
            logging.critical(e)
            return None

    def create_all_file_paths(self, asset_ids: list):
        for asset_id in asset_ids:
            self.create_file_paths(asset_id)

    def create_file_paths(self, asset_id: int):
        results = self.select_file_paths_by_id(asset_id)

        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM assets WHERE id=?', (asset_id,))
        asset = cursor.fetchone()

        if asset is None:
            logging.warning('No asset found with id: ' + str(asset_id))
            return
        else:
            asset = Asset(*asset)

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
                file_path = (asset_id, info.filename)
                file_paths.append(file_path)

        if len(results) == len(file_paths): return

        try:
            logging.debug('Creating file_paths for: ' + asset_path.name)
            cursor = self.connection.cursor()
            cursor.executemany('INSERT INTO file_paths VALUES(?,?);', file_paths)
            self.connection.commit()
        except sqlError as e:
            logging.critical(e)

    def select_file_paths_by_id(self, asset_id: int):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM file_paths WHERE asset_id=?', (asset_id,))
        results = cursor.fetchall()
        return results

    def create_source(self, title: str, path: Path):

        source = self.select_source_by_title(title)
        if source is not None:
            return source

        sql = ''' 
        INSERT INTO sources(title,path,file_count,size_raw) 
        VALUES(?,?,?,?)
        '''
        file_count = FolderHelpers.get_zip_count(path)
        size_raw = FolderHelpers.get_folder_size(path)

        source = (title, str(path), file_count, size_raw)

        try:
            cursor = self.connection.cursor()
            logging.debug('Inserting \'' + title + '\' into sources table')
            cursor.execute(sql, source)
            self.connection.commit()
            return Source(cursor.lastrowid, *source)
        except sqlError as e:
            logging.critical(e)
            return None

    def select_all_sources(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM sources')
        results = cursor.fetchall()
        sources = []
        for row in results:
            sources.append(Source(*row))

        return sources

    def select_source_by_title(self, title: str):
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM sources WHERE title=?', (title,))
            result = cursor.fetchone()
        except sqlError as e:
            logging.critical(e)
            return None

        if result is not None:
            return Source(*result)
        else:
            return None

    def select_source_by_idn(self, idn: int):
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM sources WHERE id=?', (idn,))
            result = cursor.fetchone()
        except sqlError as e:
            logging.critical(e)
            return None

        if result is not None:
            return Source(*result)
        else:
            return None

    def close(self):
        logging.info('Closing connection to database')
        self.connection.close()
