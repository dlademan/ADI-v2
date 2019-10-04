from pathlib import Path

from Handlers.Config import ConfigHandler
from Handlers.Queue import QueueHandler
from Handlers.Database import DatabaseHandler


class DataHandler:

    def __init__(self):

        self.config = ConfigHandler()

        if self.config._config is None:
            self.critical = True
            return

        self.database = DatabaseHandler()
        self.queue = QueueHandler()

        self.sources = self._create_sources()
        self.critical = False

    def close(self, position, size):
        self.config.save_config(position, size)
        self.database.close()

    def _create_sources(self):
        sources = {}
        for title, source in self.config.archives.items():
            sources[title] = self.database.create_source(title, Path(source))

        return sources
