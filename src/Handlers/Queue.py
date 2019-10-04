from pathlib import Path
from collections import OrderedDict
from Helpers import FolderHelpers


class QueueHandler:

    def __init__(self, file_name='queue.pkl'):
        self.file_name = file_name
        self.path = FolderHelpers.get_user_folder() / file_name

        self.dict = []
        self.in_progress = False
        self.save()

    def save(self):
        pass
