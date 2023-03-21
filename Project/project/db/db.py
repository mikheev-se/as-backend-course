from requests import Session
from sqlalchemy import create_engine
from project.core.settings import settings
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.db_url)

Session = sessionmaker(engine, autocommit=False, autoflush=False)


def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()
