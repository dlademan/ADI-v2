from pathlib import Path
from Config import ConfigHandler


class AssetLibrary:

    def __init__(self, sort_method='name', sort_descending=False):

        self.sort_method: str = sort_method
        self.sort_descending: bool = sort_descending

