import logging
from Config import ConfigHandler
from QueueHandler import QueueHandler
from Database import DatabaseHandler


class DataHandler:

    def __init__(self, debug):

        self.config = ConfigHandler(debug)
        self.database = DatabaseHandler()
        self.queue = QueueHandler()

    def close(self):
        self.config.save_config()
        self.database.close()

