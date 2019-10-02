import logging
from Config import ConfigHandler
from QueueHandler import QueueHandler
from Database import DatabaseHandler


class DataHandler:

    def __init__(self):

        self.config = ConfigHandler()
        self.database = DatabaseHandler()
        self.queue = QueueHandler()

    def close(self, position, size):
        self.config.save_config(position, size)
        self.database.close()

