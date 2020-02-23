import logging
import sqlite3
from pathlib import Path
from sqlite3 import Error as sqlError

from SQLHandlers.Assets import Assets
from SQLHandlers.FilePaths import FilePaths
from SQLHandlers.Folders import Folders
from SQLHandlers.Metas import Metas
from SQLHandlers.Sources import Sources

from Helpers import FolderHelpers


class SQLHandler:

    def __init__(self, filename: str = 'assets.db'):
        self.filename: str = filename
        self.path: Path = FolderHelpers.get_user_folder() / filename

        self.connection = self._init_connection()
        self._init_tables()

        if self.connection is not None:
            self.connection.commit()

        self.assets: Assets = Assets(self.connection)
        self.file_paths: FilePaths = FilePaths(self.connection, self.assets)
        self.folders: Folders = Folders(self.connection)
        self.metas: Metas = Metas(self.connection, self.assets)
        self.sources: Sources = Sources(self.connection)

    def _init_connection(self):

        connection = None
        try:
            connection = sqlite3.connect(str(self.path))
            logging.debug("Connection created to " + self.filename)
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

    def close(self):
        logging.debug('Closing connection to database')
        self.connection.close()
