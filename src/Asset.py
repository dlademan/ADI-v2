from pathlib import Path


class Asset:

    def __init__(self, idn: int, sku: int, product_name: str,
                 path: Path, filename: str, zip_size: int, installed: bool):

        self.idn = idn
        self.sku = sku
        self.product_name = product_name
        self.path = path
        self.filename = filename
        self.zip_size = zip_size
        self.installed = installed
