from pathlib import Path

from Helpers import FolderHelpers
from SQLClasses import QueueItem


class QueueHandler:

    def __init__(self):
        self.list = []

    def append(self, asset_id: int, process: int):

        pos = len(self.list)
        queue_item = QueueItem(asset_id, process, False, pos)

        self.list.append(queue_item)

    def save(self):
        pass
