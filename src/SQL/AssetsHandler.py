# AssetsHandler.py
import logging

from sqlalchemy import and_
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import sessionmaker, Session

from src.SQL import Helpers
from src.SQL.SQLHandler import Asset


class AssetsHandler:

    def __init__(self, engine):
        self.engine = engine

    def create(self,
               source_id: int,
               sku: int,
               product_name: str,
               path: str,
               filename: str,
               zip_size: int,
               installed: bool = False):

        session: Session = sessionmaker(bind=self.engine)()

        parameters = and_(Asset.filename == filename, Asset.zip_size == zip_size)
        asset = session.query(Asset).filter_by(parameters)
        if asset is None:
            asset = Asset(source_id=source_id,sku=sku, product_name=product_name,
                          path=path, filename=filename,
                          zip_size=zip_size, installed=installed)

            Helpers.commit(session, asset)

        return asset
