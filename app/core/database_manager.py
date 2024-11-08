from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .config import settings


class DatabaseManager:
    def __init__(self):
        self.client = None
        self.database = None

    def init_database(self):
        db_engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

        db: Session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)()

        try:
            yield db
        finally:
            db.close()


def get_db():
    db_manager = DatabaseManager()
    return next(db_manager.init_database())

