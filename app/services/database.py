from contextlib import contextmanager
from typing import Any, Dict

import sqlalchemy
from sqlalchemy import JSON, MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, declarative_base, sessionmaker

from app import settings

metadata = MetaData()


class Base(DeclarativeBase):
    type_annotation_map = {
        Dict[str, Any]: JSON
    }


engine = create_engine(settings.DATABASE_URL, future=True, echo=False if settings.PROD == '1' else True)
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


class DatabaseWork:
    @staticmethod
    def get_or_create(session, model, dict_for_get: dict, dict_for_create: dict):
        instance = session.query(model).filter_by(**dict_for_get).first()
        if instance:
            return instance
        else:
            instance = model(**dict_for_create)
            session.add(instance)
            session.commit()
            return instance

