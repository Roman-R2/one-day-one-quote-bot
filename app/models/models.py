import uuid
from datetime import datetime
from typing import List

from sqlalchemy import (BIGINT, BOOLEAN, DOUBLE_PRECISION, SMALLINT, TIMESTAMP,
                        UUID, VARCHAR, BigInteger, Boolean, Column, Date,
                        DateTime, ForeignKey, ForeignKeyConstraint, Integer,
                        MetaData, PrimaryKeyConstraint, SmallInteger, String,
                        Table, Text, UniqueConstraint, func)
from sqlalchemy.orm import (Mapped, backref, declared_attr, mapped_column,
                            relationship)

from app.models.abstract_models import ExtendedBase


class Quotes(ExtendedBase):
    """ Таблица содержит информацию об ответственных по ПТК. """
    __tablename__ = 'quotes'

    quote: Mapped[str] = mapped_column(Text, nullable=False, comment='Цитата')
    owner: Mapped[str] = mapped_column(Text, nullable=False, comment='Кому приписывается цитата')
