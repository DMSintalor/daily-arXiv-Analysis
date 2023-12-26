import sqlalchemy.engine.base
from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


class MySQLController:
    def __init__(self, host, username, password, db):
        self.engine = create_engine(
            f'mysql+pymysql://{username}:{password}@{host}/{db}'
        )
        self.Session = sessionmaker(bind=self.engine)
        self.Base = declarative_base()

    @contextmanager
    def get_db(self) -> sqlalchemy.orm.session.Session:
        db = self.Session(bind=self.engine.connect())
        try:
            yield db
        finally:
            db.close()

    def get_base(self):
        return self.Base

    def get_engine(self):
        return self.engine

    def create_all(self):
        self.Base.metadata.create_all(self.engine)
