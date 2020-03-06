# SourcesHandler.py
import logging
from pathlib import Path

from sqlalchemy.orm import sessionmaker, Session

from src.Helpers import SQLHelpers, FolderHelpers
from src.sql.DBClasses import Source


class SourcesHandler:

    def __init__(self, engine):
        self.engine = engine

    def __get__(self):
        session: Session = sessionmaker(bind=self.engine, expire_on_commit=False)()
        return session.query(Source).all()

    def __len__(self):
        session: Session = sessionmaker(bind=self.engine, expire_on_commit=False)()
        return session.query(Source).count()

    def __getitem__(self, source_id: int):
        session: Session = sessionmaker(bind=self.engine, expire_on_commit=False)()
        return session.query(Source).filter_by(id=source_id).first()

    def __iter__(self):
        session: Session = sessionmaker(bind=self.engine, expire_on_commit=False)()
        return session.query(Source).__iter__()

    def filter_by(self, *args, **kwargs):
        session: Session = sessionmaker(bind=self.engine, expire_on_commit=False)()
        return session.query(Source).filter_by(*args, **kwargs)

    def create(self, path: Path):
        source = self.filter_by(path_raw=str(path)).first()

        if source is not None:
            logging.debug(f'Source found: {source.path}')
            return source
        else:
            logging.debug(f'Source not found: {path}')
            file_count = FolderHelpers.get_zip_count(path)
            size_raw = FolderHelpers.get_folder_size(path)

            source = Source(path_raw=str(path), file_count=file_count, size_raw=size_raw)

            session: Session = sessionmaker(bind=self.engine, expire_on_commit=False)()
            SQLHelpers.commit(session, source)

            return source

    def update(self, path: Path):
        session: Session = sessionmaker(bind=self.engine, expire_on_commit=False)()
        source: Source = session.query(Source).filter_by(path=path)

        source.file_count = FolderHelpers.get_zip_count(path)
        source.size_raw = FolderHelpers.get_folder_size(path)

        session.commit()
