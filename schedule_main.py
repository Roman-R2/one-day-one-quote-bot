import asyncio
import datetime
from typing import Tuple

import telebot
from sqlalchemy import or_

from app import settings
from app.models.models import SendTime, Users
from app.services.app_logger import AppLogger
from app.services.database import DBAdapter
from app.services.dq_queryes import DBQueryes
from app.services.log_assistant import LogAssistant

LOGGER = AppLogger().get_logger()


async def get_tg_id_users_for_send() -> Tuple:
    with DBAdapter().get_session() as session:
        # Выбрать всех пользователей у кого сегодня не было отправки и
        today = datetime.date.today()
        now = datetime.datetime.now()
        users = session.query(SendTime, Users).join(Users).where(
            or_(
                SendTime.last_send_time == None,
                SendTime.last_send_time < today
            )
        )
        tg_ids = []
        for send_time, user in users:
            send_time: SendTime = send_time
            user: Users = user

            delta_seconds = 30
            now_set_send_time = now.replace(
                hour=send_time.set_send_time.hour,
                minute=send_time.set_send_time.minute,
                second=send_time.set_send_time.second,
                microsecond=0
            )
            if now - datetime.timedelta(seconds=delta_seconds) < now_set_send_time < now:
                tg_ids.append(user.tg_id)

    return tuple(tg_ids)


async def send_quote_for_tg_id(tg_id: id):
    """ Отправит цитату конкретному пользователю. """
    bot = telebot.TeleBot(settings.TOKEN, parse_mode="HTML")
    # Отправим цитату
    bot.send_message(chat_id=tg_id, text=DBQueryes().random_quote())
    # Добавим данные об отправки в БД
    DBQueryes.save_quote_last_send_time(tg_id=tg_id)
    return 'Complete'


async def main():
    while True:
        # Получим tg_id пользователей для отправки им цитат сейчас
        user_tg_ids = await get_tg_id_users_for_send()
        if user_tg_ids:
            print(f"{user_tg_ids=}")
            tasks = []
            for tg_id in user_tg_ids:
                tasks.append(asyncio.ensure_future(send_quote_for_tg_id(tg_id=tg_id)))
            some = await asyncio.gather(*tasks)
            print(f"{some=}")

        await asyncio.sleep(5)


try:
    LogAssistant.put_to_log(logger=LOGGER, with_print=True,
                            message=f'Запускаем schedule-app')
    asyncio.run(main())
except Exception:
    LogAssistant.put_to_log(logger=LOGGER, message=f'Неотловленная ошибка schedule-app.',
                            with_print=True, with_trace=True)
