import logging
from pathlib import Path
from sqlite3 import Error as sqlError

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from Helpers import FolderHelpers

Base = declarative_base()


class SQLHandler:

    def __init__(self, filename: str = 'assets.db'):
        self.filename: str = filename
        self.path: Path = FolderHelpers.get_user_folder() / filename

        if self.path.exists():
            self.engine = create_engine(f'sqlite:///{self.path}')
        else:
            self.engine = create_engine(f'sqlite:///{self.path}')
            Base.metadata.create_all(self.engine)


class Asset(Base):

    __tablename__ = 'assets'

    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey('sources.id'))
    sku = Column(Integer)
    product_name = Column(String)
    path = Column(String)
    filename = Column(String, unique=True)
    zip_size = Column(Integer, unique=True)
    installed = Column(Boolean)

    source = relationship('Source')

    def __repr__(self):
        return f'Asset: {self.sku} {self.product_name}'


class Tag(Base):

    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    tag = Column(String)

    def __repr__(self):
        return f'Tag: {self.tag}'


class FilePath(Base):

    __tablename__ = 'file_paths'

    asset_id = Column(Integer, ForeignKey('assets.id'), primary_key=True, unique=True)
    file_path = Column(String, unique=True)

    asset = relationship('Asset')

    def __repr__(self):
        return f'file_path: {self.asset_id}: {self.file_path}'


class AssetTag(Base):

    __tablename__ = 'asset_tags'

    asset_id = Column(Integer, ForeignKey('assets.id'))
    tag_id = Column(Integer, ForeignKey('tags.id'))

    asset = relationship('Asset')
    tag = relationship('Tag')


class Folder(Base):

    __tablename__ = 'folders'

    id = Column(Integer, primary_key=True, unique=True)
    source_id = Column(Integer, ForeignKey('sources.id'), unique=True)
    path = Column(String, unique=True)
    title = Column(String)
    file_count = Column(Integer)
    size_raw = Column(Integer)

    source = relationship('Source')

    def __repr__(self):
        return f'folder: {self.path}'


class Source(Base):

    __tablename__ = 'sources'

    id = Column(Integer, primary_key=True, unique=True)
    path = Column(String, unique=True)
    file_count = Column(Integer)
    size_raw = Column(Integer)

    def __repr__(self):
        return f'source: {self.path}'


class Meta(Base):

    __tablename__ = 'metas'

    asset_id = Column(Integer, ForeignKey('assets.id'), unique=True)
    path = Column(String, unique=True)
    imported = Column(Boolean)

    asset = relationship('Asset')


class QueueItem(Base):

    __tablename__ = 'queue_items'

    asset_id = Column(Integer, ForeignKey('assets.id'), unique=True)
    process = Column(Integer, unique=True)
    status = Column(Integer, unique=True)
    position = Column(Integer)

    asset = relationship('Asset')