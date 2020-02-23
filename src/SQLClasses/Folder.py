from pathlib import Path


class Folder:

    def __init__(self,
                 id_: int, source_id: int,
                 path: str, title: str,
                 file_count: int, size_raw: int):

        self.id_ = id_
        self.path = Path(path)
        self.title = title
        self.file_count = file_count
        self.size_raw = size_raw
        self.source_id = source_id

    def get_size(self, places=2):

        rnd = places * 10

        if self.size_raw > 2 ** 30:
            size = self.size_raw / 2 ** 30
            ext = ' GB'
        else:
            size = self.size_raw / 2 ** 20
            ext = ' MB'

        return str(int(size * rnd) / rnd) + ext
