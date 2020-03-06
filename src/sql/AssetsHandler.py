# AssetsHandler.py
import logging
from pathlib import Path


from sqlalchemy.orm import sessionmaker, Session

from sql.DBClasses import Asset
from Helpers import FileHelpers, SQLHelpers


class AssetsHandler:

    def __init__(self, engine):
        self.engine = engine

    def __len__(self):
        session: Session = sessionmaker(bind=self.engine, expire_on_commit=False)()
        return int(session.query(Asset).count())

    def __getitem__(self, asset_id):
        session: Session = sessionmaker(bind=self.engine, expire_on_commit=False)()
        return session.query(Asset).filter_by(id=asset_id).first()

    def __iter__(self):
        session: Session = sessionmaker(bind=self.engine, expire_on_commit=False)()
        return session.query(Asset).__iter__()

    @property
    def all(self):
        session: Session = sessionmaker(bind=self.engine, expire_on_commit=False)()
        return session.query(Asset).all()

    def filter_by(self, *args, **kwargs):
        session: Session = sessionmaker(bind=self.engine, expire_on_commit=False)()
        return session.query(Asset).filter_by(*args, **kwargs)

    def create(self, path: Path, source_id: int):

        if path.suffix != '.zip':
            logging.critical('Path provided does not point to a zip file')
            return None

        asset = self.filter_by(filename=str(path.name)).first()  # check if asset already exists in db

        if asset is None:
            sku = FileHelpers.get_sku(path)
            product_name = FileHelpers.parse_product_name(path)
            path_raw = str(path)
            filename = path.name
            size_raw = FileHelpers.get_file_size(path)
            installed_raw = False  # todo check if asset is already installed
            imported_raw = False

            asset = Asset(source_id=source_id,
                          sku=sku,
                          product_name=product_name,
                          path_raw=path_raw,
                          filename=filename,
                          size_raw=size_raw,
                          installed_raw=installed_raw,
                          imported_raw=imported_raw)

            session: Session = sessionmaker(bind=self.engine, expire_on_commit=False)()
            SQLHelpers.commit(session, asset)

        return asset

    def update(self, asset_id: int, **kwargs):
        session: Session = sessionmaker(bind=self.engine)()
        asset = session.query(Asset).filter_by(id=asset_id).first()

        for key, val in kwargs.items():
            setattr(asset, key, val)

        SQLHelpers.commit(session)
