from Asset import AssetLibrary
from Config import ConfigHandler
from Queue import QueueHandler
from Database import DatabaseHandler


class DataHandler:

    def __init__(self):

        self.config = ConfigHandler(self)
        self.assets = AssetLibrary(self.config)
        self.queue = QueueHandler(self.config.get_user_folder())
        self.database = DatabaseHandler(self.config.get_user_folder())
