from typing import Optional
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import database_exists, create_database
from alembic.config import Config

SessionType = Session
config = Config('./alembic.ini')

__version__ = "0.1.0"

url = config.get_main_option("sqlalchemy.url")
if url is None:
    raise Exception('Could not read alembic.ini')
engine: Engine = create_engine(url, echo=False)
inspector = inspect(engine)
Session = sessionmaker(bind=engine)
Base = declarative_base()


def validate_database():
    if not database_exists(engine.url):
        print('Database does not exist')
        print('Initializing Database')
        create_database(engine.url)


class SessionContext(object):
    def __init__(self, session: Optional[SessionType] = None):
        if session is not None:
            self.session = session
            self.close_con = False
        else:
            self.session = Session()
            self.close_con = True

    def __enter__(self) -> SessionType:
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        if self.close_con:
            self.session.flush()
            self.session.commit()
            self.session.close()
