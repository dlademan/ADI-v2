import os
import logging
from shutil import copyfileobj
from pathlib import Path
from zipfile import ZipFile

from Helpers import FileHelpers, FolderHelpers

from handlers.Config import ConfigHandler
from handlers.Queue import QueueHandler

from sql.DBHandler import DBHandler
from sql.AssetsHandler import Asset


class DataHandler:

    def __init__(self):

        self.config = ConfigHandler()

        if self.config.critical is True:
            return

        self.db = DBHandler()
        self.queue = QueueHandler()

        self._create_sources()
        self._create_libraries()
        self.critical = False

    def close(self, position, size):
        self.config.save_config(position, size)

    def _create_sources(self):
        for title, path in self.config.sources.items():
            self.db.sources.create(Path(path))

    def _create_libraries(self):
        for title, path in self.config.libraries.items():
            self.db.libraries.create(Path(path))

    def install_asset(self, asset: Asset, library_path: Path):
        logging.debug('Current library_path: ' + str(library_path))
        logging.info('Installing: ' + asset.product_name)

        with ZipFile(asset.path) as file:

            for info in file.infolist():
                if info.is_dir() or 'Manifest.dsx' in info.filename or 'Supplement.dsx' in info.filename: continue

                source = file.open(info.filename)
                local_path = Path(FileHelpers.clean_path(info.filename))
                absolute_path: Path = library_path / local_path

                root = Path(str(local_path)[:23])
                match = Path('Runtime/Support/')

                if root == match and absolute_path.suffix == '.dsx':
                    meta = str(absolute_path.stem)

                try:
                    if not absolute_path.parent.exists():
                        absolute_path.parent.mkdir(parents=True)
                    with source, open(str(absolute_path), 'wb') as out: copyfileobj(source, out)
                    self.db.file_paths.create(asset.id, str(local_path))
                except OSError as e:
                    logging.error('Error occurred during zip member extraction')
                    logging.error(e)

        self.db.assets.update(asset.id, installed_raw=True, meta=meta, img_path_raw=img_path)

        logging.info('Finished Install')

    def uninstall_asset(self, asset: Asset, library_path: Path):
        logging.debug('Current library_path: ' + str(library_path))
        logging.info('Uninstalling: ' + asset.product_name)

        file_paths = self.db.file_paths.filter_by(asset_id=asset.id)

        for file_path in file_paths:
            absolute_path = library_path / file_path.path

            try:
                os.remove(absolute_path)
            except OSError as e:
                logging.error('Could not delete file ' + absolute_path.name)

        FolderHelpers.delete_empty_dirs(library_path)
        self.db.assets.update(asset.id, installed_raw=False)
        logging.info('Finished uninstall')

    def write_meta_import_script(self, assets):
        logging.info('Writing meta_import script')
        file_path = str(self.config.import_script_path)

        try:
            with open(file_path, 'w+') as file:
                file.write('var oAssetMgr = App.getAssetMgr();\n')
                for asset in assets:
                    file.write(f'oAssetMgr.queueDBMetaFile( "{asset.img}" );\n')
        except OSError as e:
            logging.error(e)

    def execute_meta_import_script(self):
        logging.info('Launching daz to execute meta_import script')
        os.system('start ' + str(self.config.import_script_path))

