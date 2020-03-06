# QueueItemsHandler.py
import logging
from pathlib import Path

from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import sessionmaker, Session, joinedload

from src.Helpers import SQLHelpers, FolderHelpers
from src.sql.DBClasses import QueueItem, Asset


class QueueItemsHandler:

    def __init__(self, engine):
        self.engine = engine

    def __get__(self):
        session: Session = sessionmaker(bind=self.engine)()
        return session.query(QueueItem).order_by(QueueItem.position)

    def __len__(self):
        session: Session = sessionmaker(bind=self.engine)()
        return session.query(QueueItem).count()

    def __getitem__(self, source_id: int):
        session: Session = sessionmaker(bind=self.engine)()
        return session.query(QueueItem).filter(QueueItem.id == source_id)

    def __iter__(self):
        session: Session = sessionmaker(bind=self.engine)()
        return session.query(QueueItem).__iter__()

    def filter_by(self, *args, **kwargs):
        session: Session = sessionmaker(bind=self.engine)()
        query = session.query(QueueItem).options(joinedload(QueueItem.asset, innerjoin=True),
                                                 joinedload(QueueItem.library, innerjoin=True))
        return query.filter_by(*args, **kwargs)

    def create(self, asset_id: int, library_id: int, process: int):
        session: Session = sessionmaker(bind=self.engine)()

        status = 0
        position = session.query(QueueItem).count()

        queue_item = QueueItem(asset_id=asset_id, library_id=library_id,
                               process_int=process, status_int=status,
                               position=position, completed_date=None)

        SQLHelpers.commit(session, queue_item)

        return queue_item

    @property
    def pending(self):
        session: Session = sessionmaker(bind=self.engine)()
        query = session.query(QueueItem).filter(QueueItem.status_int == 0)
        # query = query.options(joinedload(QueueItem.asset, innerjoin=True),)
        # query = query.options(joinedload(QueueItem.library, innerjoin=True),)
        return query.all()

    @property
    def not_pending(self):
        session: Session = sessionmaker(bind=self.engine, expire_on_commit=False)()
        query = session.query(QueueItem).options(joinedload(QueueItem.asset, innerjoin=True),)
        return query.filter(QueueItem.status_int != 0).all()
