import unittest
from pathlib import Path

from src.Database import DatabaseHandler


class TestDatabase(unittest.TestCase):

    def test_create_folder(self):

        folder_path = Path(r'D:\Files\DAZ Zips')
        user_path = Path(r'C:\Users\glavi\AppData\Roaming\ADI')
        database = DatabaseHandler(user_path)

        folder_tuple = database.create_folder(folder_path)

        self.assertEqual(len(folder_tuple), 5)       # 5 length
        self.assertIsInstance(folder_tuple, tuple)   # is a tuple
        self.assertIsInstance(folder_tuple[0], int)  # id
        self.assertIsInstance(folder_tuple[1], str)  # path
        self.assertIsInstance(folder_tuple[2], str)  # title
        self.assertIsInstance(folder_tuple[3], int)  # file_count
        self.assertIsInstance(folder_tuple[4], int)  # size_raw

        database.connection.close()

    def test_create_asset(self):

        asset_path = Path(
            r'D:\Files\DAZ Zips\Genesis 8\Female\Hair\IM00045853-01_LaineyHairforGenesis3FemalesandGenesis8Females.zip')

        user_path = Path(r'C:\Users\glavi\AppData\Roaming\ADI')
        database = DatabaseHandler(user_path)

        asset_tuple = database.create_asset(asset_path)

        # (id, sku, hash, zip_path, zip_file_name, product_name, zip_size_raw, ext_size_raw)

        self.assertEqual(len(asset_tuple), 8)  # 8 length tuple
        self.assertIsInstance(asset_tuple, tuple)  # is a tuple
        self.assertIsInstance(asset_tuple[0], int)  # id
        self.assertIsInstance(asset_tuple[1], int)  # sku
        self.assertIsInstance(asset_tuple[2], str)  # hash
        self.assertIsInstance(asset_tuple[3], str)  # path
        self.assertIsInstance(asset_tuple[4], str)  # file_name
        self.assertIsInstance(asset_tuple[5], str)  # product_name
        self.assertIsInstance(asset_tuple[6], int)  # zip_size_raw
        self.assertIsInstance(asset_tuple[7], int)  # ext_size_raw

        database.connection.close()
