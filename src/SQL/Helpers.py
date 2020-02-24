# Helpers.py
import logging
from sqlalchemy.exc import DatabaseError


def commit(session, row=None):
    try:
        if row is not None:
            session.add(row)
        session.commit()
    except DatabaseError as e:
        logging.critical(e)
        session.rollback()
    finally:
        session.close()