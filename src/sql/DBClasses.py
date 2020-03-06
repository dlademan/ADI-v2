import logging
from pathlib import Path
from sqlite3 import Error as sqlError
from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from Helpers import FileHelpers

Base = declarative_base()


class Asset(Base):

    __tablename__ = 'assets'

    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey('sources.id'))

    sku = Column(Integer)
    product_name = Column(String)
    filename = Column(String, unique=True)

    path_raw = Column(String)

    size_raw = Column(Integer)
    installed_raw = Column(Boolean)
    imported_raw = Column(Boolean)

    meta = Column(String, nullable=True)
    img = Column(String, nullable=True)

    source = relationship('Source')

    def __repr__(self):
        return f'{self.product_name}'

    @property
    def path(self):
        return Path(self.path_raw)

    @property
    def size(self, places=2):
        return FileHelpers.format_bytes(self.size_raw, places)

    @property
    def installed(self):
        text = 'Not' if not self.installed_raw else 'Installed'
        return text

    # @property
    # def sku(self):
    #     if self.sku == 0:
    #         return 'null'
    #     else:
    #         return str(self.sku)


class Tag(Base):

    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    tag = Column(String)

    def __repr__(self):
        return f'Tag: {self.tag}'


# class AssetTag(Base):
#
#     __tablename__ = 'asset_tags'
#
#     asset_id = Column(Integer, ForeignKey('assets.id'))
#     tag_id = Column(Integer, ForeignKey('tags.id'))
#
#     asset = relationship('Asset')
#     tag = relationship('Tag')


class FilePath(Base):

    __tablename__ = 'file_paths'

    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey('assets.id'))
    path = Column(String)

    asset = relationship('Asset')

    __table_args__ = (UniqueConstraint('asset_id', 'path', name='_asset_path_uc'),)

    def __repr__(self):
        return f'file_path: {self.asset_id}: {self.path}'


class Folder(Base):

    __tablename__ = 'folders'

    id = Column(Integer, primary_key=True, unique=True)
    source_id = Column(Integer, ForeignKey('sources.id'))
    path_raw = Column(String, unique=True)
    title = Column(String)
    file_count = Column(Integer)
    size_raw = Column(Integer)

    source = relationship('Source')

    def __repr__(self):
        return f'folder: {self.path}'

    @property
    def path(self):
        return Path(self.path_raw)

    @property
    def size(self, places=2):
        return FileHelpers.format_bytes(self.size_raw, places)


class Source(Base):

    __tablename__ = 'sources'

    id = Column(Integer, primary_key=True, unique=True)
    path_raw = Column(String, unique=True)
    file_count = Column(Integer)
    size_raw = Column(Integer)

    def __repr__(self):
        return f'source: {self.path}'

    @property
    def path(self):
        return Path(self.path_raw)

    @property
    def size(self, places=2):
        return FileHelpers.format_bytes(self.size_raw, places)


class QueueItem(Base):

    __tablename__ = 'queue_items'

    id = Column(Integer, primary_key=True)
    asset_id = Column(ForeignKey('assets.id'))
    library_id = Column(ForeignKey('libraries.id'))
    process_int = Column(Integer)
    status_int = Column(Integer)
    position = Column(Integer)
    completed_date = Column(DateTime, nullable=True)

    __table_args__ = (UniqueConstraint('asset_id', 'process_int', 'status_int', name='_asset_process_status_uc'),)

    asset = relationship('Asset', backref=backref("queue_items", order_by=id))
    library = relationship('Library')

    def __repr__(self):
        return f'QueueItem: {self.asset.product_name} - {self.status} {self.process}'

    @property
    def process(self):
        processes = ['Install', 'Uninstall']
        return processes[self.process_int]

    @property
    def status(self):
        statuses = ['Pending', 'In Progress', 'Completed', 'Failed']
        return statuses[self.status_int]

    @property
    def completed(self):
        return self.completed_date.strftime("%b %d %H:%M:%S") if self.completed_date is not None else None


class Library(Base):

    __tablename__ = 'libraries'

    id = Column(Integer, primary_key=True)
    path_raw = Column(String, unique=True)
    assets_installed = Column(Integer)
    size_raw = Column(Integer)

    @property
    def size(self, places=2):
        return FileHelpers.format_bytes(self.size_raw, places)

    @property
    def path(self):
        return Path(self.path_raw)
