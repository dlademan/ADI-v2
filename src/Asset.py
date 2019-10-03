from pathlib import Path


class Asset:

    def __init__(self, idn: int, parent: int,
                 sku: int, product_name: str,
                 path: str, filename: str,
                 size_raw: int, installed: bool):

        self.idn = idn
        self.parent = parent
        self.sku = sku
        self.product_name = product_name
        self.path = Path(path)
        self.filename = filename
        self.size_raw = size_raw
        self.installed = installed

    def get_size(self, places=2):

        rnd = places * 10

        if self.size_raw > 2 ** 30:
            size = self.size_raw / 2 ** 30
            ext = ' GB'
        else:
            size = self.size_raw / 2 ** 20
            ext = ' MB'

        return str(int(size * rnd) / rnd) + ext

    def get_installed(self):
        text = 'Not installed' if not self.installed else 'Installed'
        return text
