import logging
from pathlib import Path
from sqlite3 import Error as sqlError

from SQLClasses.Source import Source
from Helpers import FolderHelpers


class Sources:

    def __init__(self, connection):
        self.connection = connection

    def create_source(self, path: Path):

        source = self.select_source_by_path(str(path))
        if source is not None:
            return source

        sql = ''' 
        INSERT INTO sources(path,file_count,size_raw) 
        VALUES(?,?,?)
        '''
        file_count = FolderHelpers.get_zip_count(path)
        size_raw = FolderHelpers.get_folder_size(path)

        source = (str(path), file_count, size_raw)

        try:
            cursor = self.connection.cursor()
            logging.debug('Inserting \'' + path.name + '\' into sources table')
            cursor.execute(sql, source)
            self.connection.commit()
            return Source(cursor.lastrowid, *source)
        except sqlError as e:
            logging.critical(e)
            return None

    def update_source_by_path(self, path):
        source: Source = self.select_source_by_path(path)
        source.update()

        sql = ''' 
                UPDATE sources
                SET file_count = ?
                SET size_raw = ?
                WHERE id = ?
                '''

        values = (source.file_count, source.size_raw, source.id_)

        try:
            cursor = self.connection.cursor()
            logging.debug('Source: ' + source.path.name)
            logging.debug('Updating file_count to: ' + str(source.file_count))
            logging.debug('Updating size_raw to: ' + str(source.size_raw))
            cursor.execute(sql, values)
            self.connection.commit()
        except sqlError as e:
            logging.critical(e)

    def select_source_by_path(self, path: str):
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM sources WHERE path=?', (path,))
            result = cursor.fetchone()
        except sqlError as e:
            logging.critical(e)
            return None

        if result is not None:
            return Source(*result)
        else:
            return None

    def select_source_by_id(self, idn: int):
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

    def select_all_sources(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM sources')
        results = cursor.fetchall()
        sources = []
        for row in results:
            sources.append(Source(*row))

        return sources
