from Handlers.Config import ConfigHandler
from Handlers.Queue import QueueHandler
from Handlers.Database import DatabaseHandler


class DataHandler:

    def __init__(self):

        self.config = ConfigHandler()
        self.database = DatabaseHandler()
        self.queue = QueueHandler()

    def close(self, position, size):
        self.config.save_config(position, size)
        self.database.close()

