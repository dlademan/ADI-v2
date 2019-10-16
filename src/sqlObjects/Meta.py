from pathlib import Path


class Meta:

    def __init__(self, asset_id: int, product: str, imported: bool):

        self.asset_id = asset_id
        self.product = product
        self.imported = imported
