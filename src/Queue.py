from pathlib import Path
from collections import OrderedDict


class QueueHandler:

    def __init__(self, user_folder: Path, file_name='queue.pkl'):
        self.file_name = file_name
        self.path = user_folder / file_name

        self.dict = []
        self.in_progress = False
        self.save()

    def save(self):
        pass
