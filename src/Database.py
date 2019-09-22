import sqlite3
from sqlite3 import Error as sqlError
from pathlib import Path
from Config import ConfigHandler


class DatabaseHandler:

    def __init__(self, user_folder: Path, file_name='assets.db'):
        self.file_name: str = file_name
        self.path: Path = user_folder / file_name

        self.conn = self._create_connection()
        self._create_tables()

        self._create_asset((0, 'path/to/file/', 'file_name.ext', 'product_name', 100, 200))

        self.conn.commit()
        self.conn.close()

    def _create_connection(self):

        conn = None
        try:
            conn = sqlite3.connect(str(self.path))
            print("Connection created to " + self.file_name)
            print("SQLite version: " + sqlite3.version)
        except sqlError as e:
            print(e)

        return conn

    def _create_table(self, table_name, sql_table):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql_table)
        except sqlError as e:
            print(table_name + ": ")
            print(e)

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
            print("Error! Cannot create the database connection.")

    def _create_asset(self, asset: tuple):

        sql = ''' 
        INSERT INTO assets(sku,zip_path,zip_file_name,product_name,zip_size_raw,ext_size_raw) 
        VALUES(?,?,?,?,?,?)
        '''
        cursor = self.conn.cursor()
        try:
            print('Inserting ' + asset[3] + ' into assets table')
            cursor.execute(sql, asset)
        except sqlError as e:
            print(e)
        print(cursor.lastrowid)
        return cursor.lastrowid
