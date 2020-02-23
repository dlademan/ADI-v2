import logging
from pathlib import Path
from sqlite3 import Error as sqlError

from SQLClasses.Folder import Folder
from Helpers import FolderHelpers


class Folders:

    def __init__(self, connection):
        self.connection = connection

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

    def select_folder_by_id(self, folder_id: int):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM folders WHERE id=?', (folder_id,))
        return Folder(*cursor.fetchone())

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

    def select_all_folders_by_source_id(self, source_id: int):
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM folders WHERE source_id=?', (source_id,))
            return cursor.fetchall()
        except sqlError as e:
            logging.critical(e)
            return None
