import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import (BIGINT, BOOLEAN, DOUBLE_PRECISION, SMALLINT, TIMESTAMP,
                        UUID, VARCHAR, BigInteger, Boolean, Column, Date,
                        DateTime, ForeignKey, ForeignKeyConstraint, Integer,
                        MetaData, PrimaryKeyConstraint, SmallInteger, String,
                        Table, Text, UniqueConstraint, func, TIME)
from sqlalchemy.orm import (Mapped, backref, declared_attr, mapped_column,
                            relationship)

from app.models.abstract_models import ExtendedBase, ExtendedBaseWithTime


class Quotes(ExtendedBase):
    """ Модель содержит информацию об ответственных по ПТК. """
    __tablename__ = 'quotes'

    quote: Mapped[str] = mapped_column(Text, nullable=False, comment='Цитата')
    owner: Mapped[str] = mapped_column(Text, nullable=False, comment='Кому приписывается цитата')


class Users(ExtendedBaseWithTime):
    # {'id': 232597319, 'is_bot': False, 'first_name': 'Roman Sl', 'username': 'Roman_R2Z',
    # 'last_name': None, 'language_code': 'ru', 'can_join_groups': None, 'can_read_all_group_messages': None,
    # 'supports_inline_queries': None, 'is_premium': None, 'added_to_attachment_menu': None, 'can_connect_to_business': None}`
    """ Модель содержит информацию о пользователях бота. """
    __tablename__ = 'users'

    tg_id: Mapped[int] = mapped_column(Integer, nullable=False, comment='Id telegram user')
    is_bot: Mapped[bool] = mapped_column(Boolean, nullable=False, comment='telegram user is bot')
    username: Mapped[str] = mapped_column(String, nullable=False, comment='Username of telegram user')
    first_name: Mapped[Optional[str]] = mapped_column(String, comment='User first name')
    last_name: Mapped[Optional[str]] = mapped_column(String, comment='User last name')
    language_code: Mapped[Optional[str]] = mapped_column(String, comment='User language code')


class SendTime(ExtendedBaseWithTime):
    """ Модель содержит привязку времени отправки к конкретному пользователю. """
    __tablename__ = 'send_time'

    send_time = Column(TIME, nullable=False)
    user: Mapped[UUID] = mapped_column(ForeignKey(Users.id), nullable=False, comment='User FK')
