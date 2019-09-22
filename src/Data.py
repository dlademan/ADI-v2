import logging
from Asset import AssetLibrary
from Config import ConfigHandler
from Queue import QueueHandler
from Database import DatabaseHandler


class DataHandler:

    def __init__(self):

        self.config = ConfigHandler()
        self.database = DatabaseHandler(self.config.user_folder_path)
        self.assets = AssetLibrary()
        self.queue = QueueHandler(self.config.user_folder_path)
