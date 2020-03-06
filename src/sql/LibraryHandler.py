# LibrariesHandler.py
import logging
from pathlib import Path

from sqlalchemy.orm import sessionmaker, Session

from src.Helpers import SQLHelpers, FolderHelpers
from src.sql.DBClasses import Library


class LibrariesHandler:

    def __init__(self, engine):
        self.engine = engine

    def __iter__(self):
        session: Session = sessionmaker(bind=self.engine, expire_on_commit=False)()
        return session.query(Library).__iter__()

    def filter_by(self, *args, **kwargs):
        session: Session = sessionmaker(bind=self.engine, expire_on_commit=False)()
        return session.query(Library).filter_by(*args, **kwargs)

    def create(self, path: Path):
        library = self.filter_by(path_raw=str(path)).first()

        if library is not None:
            logging.debug(f'Library found: {library.path}')
            return library
        else:
            logging.debug(f'Library not found: {path}')
            size_raw = FolderHelpers.get_folder_size(path)

            library = Library(path_raw=str(path), assets_installed=0, size_raw=size_raw)

            session: Session = sessionmaker(bind=self.engine, expire_on_commit=False)()
            SQLHelpers.commit(session, library)

            return library
