from contextlib import contextmanager
from typing import Any, Dict

from sqlalchemy import JSON, MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, declarative_base, sessionmaker

from app import settings

metadata = MetaData()


class Base(DeclarativeBase):
    type_annotation_map = {
        Dict[str, Any]: JSON
    }


engine = create_engine(settings.DATABASE_URL, future=True, echo=True)
Session = sessionmaker(engine)


class DBAdapter:
    @contextmanager
    def get_session(self):
        session = Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
