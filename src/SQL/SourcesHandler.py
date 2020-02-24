# AssetsHandler.py
import logging

from sqlalchemy import and_
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import sessionmaker, Session

from src.SQL import Helpers
from src.SQL.SQLHandler import Source


class SourcessHandler:

    def __init__(self, engine):
        self.engine = engine

    def create(self,