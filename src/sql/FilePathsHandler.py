# FilePathsHandler.py
import logging
from pathlib import Path
from zipfile import ZipFile, BadZipFile

from sqlalchemy import and_
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import sessionmaker, Session

from src.sql.DBClasses import FilePath, Asset
from src.Helpers import SQLHelpers, FolderHelpers, FileHelpers


class FilePathsHandler:

    def __init__(self, engine):
        self.engine = engine

    def filter_by(self, *args, **kwargs):
        session: Session = sessionmaker(bind=self.engine)()
        return session.query(FilePath).filter_by(*args, **kwargs)

    def create(self, asset_id, path: str = None):
        session: Session = sessionmaker(bind=self.engine)()

        if path is not None:  # single path creation
            file_path = self.filter_by(asset_id=asset_id, path=path).first()
            if file_path is None:
                file_path = FilePath(asset_id=asset_id, path=path)
                SQLHelpers.commit(session, file_path)
            return file_path

        else:
            current_len = self.filter_by(asset_id=asset_id).count()
            asset: Asset = session.query(Asset).filter_by(id=asset_id)

            asset_path = asset.path_raw / asset.filename

            try:
                with ZipFile(asset.path_raw / asset.filename) as asset_zip_file:
                    if current_len == len(asset_zip_file.infolist()): return
                    info_list = asset_zip_file.infolist()
            except BadZipFile as e:
                logging.error('Error occurred while opening zip file: ' + str(asset_path.name))
                logging.error(e)
                logging.info('File paths not created for: ' + str(asset_path.name))
                return

            file_paths_list = []
            for info in info_list:
                if not info.is_dir():
                    file_path = FilePath(asset_id, FileHelpers.clean_path(info.filename))
                    file_paths_list.append(file_path)

            session.bulk_save_objects(file_paths_list)
            SQLHelpers.commit(session)