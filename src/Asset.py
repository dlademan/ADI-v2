from pathlib import Path


class Asset:

    def __init__(self, idn: int, sku: int, product_name: str,
                 path: Path, filename: str, size_raw: int, installed: bool):

        self.idn = idn
        self.sku = sku
        self.product_name = product_name
        self.path = path
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
