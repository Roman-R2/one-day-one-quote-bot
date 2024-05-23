import uuid
from datetime import datetime
from typing import Any, Dict

from sqlalchemy import UUID, Column, DateTime, Float, String, func
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.orm import Mapped, mapped_column

from app.services.database import Base


class ExtendedBase(Base):
    """ Абстрактный класс для расширения моделей id. """
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class ExtendedBaseWithTime(ExtendedBase):
    """ Абстрактный класс для расширения моделей. """
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), comment='Создно')
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        # nullable=True,
        comment='Обновлено'
    )
