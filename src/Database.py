import logging
import sqlite3
from sqlite3 import Error as sqlError
from pathlib import Path


class DatabaseHandler:

    def __init__(self, user_folder: Path, file_name: str = 'assets.db'):
        self.file_name: str = file_name
        self.path: Path = user_folder / file_name

        self.conn = self._create_connection()
        self._create_tables()

        self.conn.commit()
        self.conn.close()

    def _create_connection(self):

        conn = None
        try:
            conn = sqlite3.connect(str(self.path))
            logging.info("Connection created to " + self.file_name)
            logging.info("SQLite version: " + sqlite3.version)
        except sqlError as e:
            logging.critical(e)

        return conn

    def _create_table(self, table_name, sql_table):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql_table)
        except sqlError as e:
            logging.info(table_name + ": ")
            logging.info(e)

    def _create_tables(self):
        tables = []

        with open('tables', 'r') as tables_file:
            for line in tables_file:
                if line[:12] == 'CREATE TABLE':
                    tables.append('')
                    tables[-1] += line
                    continue
                elif line == '\n': continue
                else: tables[-1] += line

        if self.conn is not None:
            for i, table in enumerate(tables):
                self._create_table("Table " + str(i), table)
        else:
            logging.critical("Error! Cannot create the database connection.")

    def create_asset(self, asset: tuple):

        sql = ''' 
        INSERT INTO assets(sku,zip_path,zip_file_name,product_name,zip_size_raw,ext_size_raw) 
        VALUES(?,?,?,?,?,?)
        '''
        cursor = self.conn.cursor()
        try:
            logging.info('Inserting ' + asset[3] + ' into assets table')
            cursor.execute(sql, asset)
        except sqlError as e:
            logging.critical(e)
        return cursor.lastrowid
