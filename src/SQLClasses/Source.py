from pathlib import Path
from Helpers import FolderHelpers


class Source:

    def __init__(self,
                 id_: int, path: str,
                 file_count: int, size_raw: int):

        self.id_ = id_
        self.path = Path(path)
        self.file_count = file_count
        self.size_raw = size_raw

    def get_array(self):
        return [self.id_, str(self.path), self.file_count, self.size_raw]
