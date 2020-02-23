import os
import logging
import shutil
from pathlib import Path
from zipfile import ZipFile

from Handlers.Config import ConfigHandler
from Handlers.Queue import QueueHandler
from SQLHandlers._SQLHandler import SQLHandler

from SQLClasses.Asset import Asset
from Helpers import FileHelpers, FolderHelpers


class MainHandler:

    def __init__(self):

        self.config = ConfigHandler()

        if self.config.critical is True:
            return

        self.sql_handler = SQLHandler()
        self.queue = QueueHandler()

        self.sources = self._create_sources()
        self.critical = False

    def close(self, position, size):
        self.config.save_config(position, size)
        self.sql_handler.close()

    def _create_sources(self):
        sources = {}
        for title, path in self.config.sources.items():
            sources[title] = self.sql_handler.sources.create_source(Path(path))

        return sources

    def install_asset(self, asset: Asset, library_path: Path):
        logging.debug('Current library_path: ' + str(library_path))
        logging.info('Installing: ' + asset.product_name)

        with ZipFile(asset.zip_path) as file:
            info_list = file.infolist()

            for info in info_list:
                if info.is_dir() or 'Manifest.dsx' in info.filename or 'Supplement.dsx' in info.filename: continue

                source = file.open(info.filename)
                local_path = Path(FileHelpers.clean_path(info.filename))
                absolute_path: Path = library_path / local_path

                if absolute_path.suffix == '.dsx' and absolute_path.parent.name == 'Support':
                    # create meta in database for later
                    self.sql_handler.metas.create_meta(asset.id_, absolute_path.stem, False)

                try:
                    if not absolute_path.parent.exists():
                        absolute_path.parent.mkdir(parents=True)
                    with source, open(str(absolute_path), 'wb') as out: shutil.copyfileobj(source, out)
                    self.sql_handler.file_paths.create_single_file_path_for_asset_id(asset.id_, local_path)
                except OSError as e:
                    logging.error('Error occurred during zip member extraction')
                    logging.error(e)

        self.sql_handler.assets.update_asset_installed(True, asset.id_)

        logging.info('Finished Install')

    def uninstall_asset(self, asset: Asset, library_path: Path):
        logging.debug('Current library_path: ' + str(library_path))
        logging.info('Uninstalling: ' + asset.product_name)

        file_paths = self.sql_handler.file_paths.select_file_paths_by_id(asset.id_)

        for file_path in file_paths:
            absolute_path = library_path / file_path[1]

            try:
                os.remove(absolute_path)
            except OSError as e:
                logging.error('Could not delete file ' + absolute_path.name)
                logging.error(e)

        FolderHelpers.delete_empty_dirs(library_path)
        self.sql_handler.assets.update_asset_installed(False, asset.id_)
        logging.info('Finished uninstall')

    def write_meta_import_script(self, metas):
        logging.info('Writing meta_import script')
        file_path = str(self.config.import_script_path)

        try:
            with open(file_path, 'w+') as file:
                file.write('var oAssetMgr = App.getAssetMgr();\n')
                for meta in metas:
                    file.write('oAssetMgr.queueDBMetaFile( "' + meta.product + '" );\n')
        except OSError as e:
            logging.error(e)

    def execute_meta_import_script(self):
        logging.info('Launching daz to execute meta_import script')
        os.system('start ' + str(self.config.import_script_path))

