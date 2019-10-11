from pathlib import Path


class Source:

    def __init__(self,
                 id_: int, title: str, path: str,
                 file_count: int, size_raw: int):

        self.id_ = id_
        self.title = title
        self.path = Path(path)
        self.file_count = file_count
        self.size_raw = size_raw
