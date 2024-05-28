import random
import time

from app.models.models import Quotes, Users, SendTime
from app.services.database import DBAdapter, DatabaseWork
from app.services.dto import UserDTO


class DBQueryes:
    def random_quote(self) -> str:
        with DBAdapter().get_session() as session:
            rand = random.randrange(0, session.query(Quotes).count())
            rand_row: Quotes = session.query(Quotes)[rand]
            return f"{rand_row.quote}\n---------------------------\n{rand_row.owner}"

    @staticmethod
    def current_user(message):
        with DBAdapter().get_session() as session:
            attrs_for_get = {
                'tg_id': message.from_user.id,
            }
            attrs_for_create = {
                'tg_id': message.from_user.id,
                'is_bot': message.from_user.is_bot,
                'username': message.from_user.username,
                'first_name': message.from_user.first_name,
                'last_name': message.from_user.last_name,
                'language_code': message.from_user.language_code,
            }
            user = DatabaseWork.get_or_create(session, Users, dict_for_get=attrs_for_get,
                                              dict_for_create=attrs_for_create)
            return UserDTO(id=user.id, tg_id=user.tg_id, username=user.username)

    @staticmethod
    def save_quote_send_time(message, user_time: time):
        with DBAdapter().get_session() as session:
            user_instance = session.query(Users).filter_by(tg_id=message.from_user.id).first()
            instance = session.query(SendTime).filter_by(user=user_instance.id).first()
            if instance:
                instance.send_time = user_time
                session.add(instance)
            else:
                session.add(SendTime(user=user_instance.id, send_time=user_time))
            session.commit()
