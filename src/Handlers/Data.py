import os
import logging
import shutil
from pathlib import Path
from zipfile import ZipFile, ZipInfo

from Handlers.Config import ConfigHandler
from Handlers.Queue import QueueHandler
from Handlers.Database import DatabaseHandler

from sqlObjects.Asset import Asset
from Helpers import FileHelpers


class DataHandler:

    def __init__(self):

        self.config = ConfigHandler()

        if self.config._config is None:
            self.critical = True
            return

        self.database = DatabaseHandler()
        self.queue = QueueHandler()

        self.sources = self._create_sources()
        self.critical = False

    def close(self, position, size):
        self.config.save_config(position, size)
        self.database.close()

    def _create_sources(self):
        sources = {}
        for title, source in self.config.archives.items():
            sources[title] = self.database.create_source(title, Path(source))

        return sources

    def install_asset(self, asset_id: int, install_path: Path):
        asset: Asset = self.database.select_asset_by_id(asset_id)

        with ZipFile(asset.zip) as file:
            info_list = file.infolist()

            for info in info_list:
                if info.is_dir() or 'Manifest.dsx' in info.filename or 'Supplement.dsx' in info.filename: continue

                source = file.open(info.filename)
                local_path = Path(FileHelpers.clean_path(info.filename))
                absolute_path: Path = install_path / local_path

                try:
                    if not absolute_path.parent.exists():
                        absolute_path.parent.mkdir(parents=True)
                    with source, open(str(absolute_path), 'wb') as out: shutil.copyfileobj(source, out)
                    self.database.create_single_file_path_for_asset_id(asset_id, local_path)
                except OSError as e:
                    logging.error('Error occurred during zip member extraction')
                    logging.error(e)

        logging.info(asset.product_name + " installed")

    # todo create uninstall
    def uninstall_asset(self, asset_id: int, install_path: Path):
        asset: Asset = self.database.select_asset_by_id(asset_id)
        file_paths = self.database.select_file_paths_by_id(asset_id)

        for file_path in file_paths:
            absolute_path = install_path / file_path[1]

            try:
                os.remove(absolute_path)
            except OSError as e:
                logging.error('Could not delete file ' + absolute_path.name)
                logging.error(e)

        logging.info(asset.product_name + " uinstalled")
