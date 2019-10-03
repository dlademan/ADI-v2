from pathlib import Path


class Folder:

    def __init__(self,
                 idn: int, source: bool, parent: int,
                 path: str, title: str,
                 file_count: int, size_raw: int):

        self.idn = idn
        self.source = source
        self.parent = parent
        self.path = Path(path)
        self.title = title
        self.file_count = file_count
        self.size_raw = size_raw
