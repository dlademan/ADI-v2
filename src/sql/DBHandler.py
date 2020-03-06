import logging
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from Helpers import FolderHelpers

from sql.AssetsHandler import AssetsHandler
from sql.SourcesHandler import SourcesHandler
from sql.FilePathsHandler import FilePathsHandler
from sql.FoldersHandler import FoldersHandler
from sql.QueueItemsHandler import QueueItemsHandler
from sql.LibraryHandler import LibrariesHandler

from sql.DBClasses import Asset


from sql.DBClasses import Base


class DBHandler:

    def __init__(self, filename: str = 'adi.db'):
        self.filename: str = filename
        self.path: Path = FolderHelpers.get_user_folder() / filename
        self.engine = create_engine(f'sqlite:///{self.path}')
        self.session: Session = sessionmaker(bind=self.engine, expire_on_commit=False)()

        if not self.path.exists():
            Base.metadata.create_all(self.engine)

        self.assets = AssetsHandler(self.engine)
        self.sources = SourcesHandler(self.engine)
        self.file_paths = FilePathsHandler(self.engine)
        self.folders = FoldersHandler(self.engine)
        self.queue = QueueItemsHandler(self.engine)
        self.libraries = LibrariesHandler(self.engine)
