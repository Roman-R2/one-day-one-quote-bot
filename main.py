import datetime
import os
import time

import requests
import telebot
from telebot import formatting, types

from app import settings
from app.models.models import Quotes
from app.services.app_logger import AppLogger
from app.services.dq_queryes import DBQueryes
from app.services.dto import UserDTO, QuotesTimeDTO
from app.services.first_fill_data import FirstFillTables
from app.services.log_assistant import LogAssistant

LOGGER = AppLogger().get_logger()


class Phrases:
    CONFIGURE_TEXT = "Настроить"
    QUOTES_SEND_TEXT = "Пришли цитату"
    RETURN_MAIN_MENY_TEXT = 'Вернуться в главное меню'
    GET_BOT_CONFIG = 'Bot check'


class ButtonsMarkup:
    @staticmethod
    def start_button_markup():
        btn_phrases = [Phrases.CONFIGURE_TEXT, Phrases.QUOTES_SEND_TEXT, Phrases.GET_BOT_CONFIG]
        keyboards = []
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for phrase in btn_phrases:
            keyboards.append(types.KeyboardButton(phrase))
        markup.add(*keyboards)
        return markup

    @staticmethod
    def send_time_button_markup():
        btn_phrases = {
            "07:00": 'assign_send_data-07:00',
            "08:00": 'assign_send_data-08:00',
            "09:00": 'assign_send_data-09:00',
            "10:00": 'assign_send_data-10:00',
            "11:00": 'assign_send_data-11:00',
            "12:00": 'assign_send_data-12:00',
            "Не отправлять больше": 'assign_send_data-no',
        }
        keyboards = []
        markup = telebot.types.InlineKeyboardMarkup()
        for text, callback_data in btn_phrases.items():
            keyboards.append(
                telebot.types.InlineKeyboardButton(text=text, callback_data=callback_data)
            )
        markup.add(*keyboards)
        return markup


class GetData:
    @staticmethod
    def for_tg_user_data(message):
        return message.id


if __name__ == '__main__':
    # Если быза данных не заполнена первичными данными, то сделаем это
    if FirstFillTables.get_quotes_table_row_count() < 1:
        print(f" Наполняем данными таблицу {Quotes.__name__}")
        FirstFillTables.fill_data()

    LogAssistant.put_to_log(logger=LOGGER, with_print=True,
                            message=f'Запускаем telebot\nPROD environment = {os.getenv("PROD")}')

    bot = telebot.TeleBot(settings.TOKEN, parse_mode="HTML")


    @bot.callback_query_handler(func=lambda call: call.data.startswith('assign_send_data'))
    def callback_inline_first(call):
        str_end = call.data.split('-')[1]
        if str_end == 'no':
            user_time = None
            message_for_user = f"Цитаты больше не будут отправляться. Вы всегда можете настроить отправку позже."
        else:
            user_time = datetime.datetime.strptime(call.data.split('-')[1], '%H:%M')
            message_for_user = f"Установили время отправки на {user_time.strftime('%H:%M')} МСК"

        DBQueryes.save_quote_set_send_time(call, user_time)

        bot.send_message(
            call.message.chat.id,
            text=message_for_user,
        )


    @bot.message_handler(commands=['start'])
    def start(message):
        # Возьмем или создадим пользовател в БД
        print(f"{message}")
        user: UserDTO = DBQueryes.current_user(message)
        DBQueryes.save_quote_set_send_time(message, settings.DEFAULT_QUOTES_SEND_TIME)
        bot.send_message(
            message.chat.id,
            text=f"Привет {formatting.hbold(user.username) if user.username else formatting.hbold(user.first_name)}.\nЯ бот, который будет присылать умную цитату в указанное время.\nРазмышляй, думай, учись.... \nВремя отправки установлено на {settings.DEFAULT_QUOTES_SEND_TIME.strftime('%H:%M')} по МСК.",
            reply_markup=ButtonsMarkup.start_button_markup()
        )


    @bot.message_handler(content_types=['text'])
    def func(message):
        def config_bot_action():
            bot.send_message(
                message.chat.id,
                text="""Выберите в какое время время по МСК прислать цитату:""",
                reply_markup=ButtonsMarkup.send_time_button_markup()
            )

        def send_quote_action():
            bot.send_message(
                message.chat.id,
                text=DBQueryes().random_quote(),
            )

        def bot_check_action():
            now_time = datetime.datetime.now()
            utcnow_time = datetime.datetime.now(datetime.UTC)
            user: UserDTO = DBQueryes.current_user(message)
            quotes_time: QuotesTimeDTO | None = DBQueryes.get_quotes_time(user_uuid=user.id)

            msg = (
                f"Локальное время сервера:\n"
                f"\t\tnow_time={formatting.hbold(str(now_time))}\n"
                f"\t\tutcnow_time={formatting.hbold(str(utcnow_time))}\n"
                f"Ваш пользователь:\n "
                f"\t\tusername={formatting.hbold(user.username)}\n"
                f"\t\tfirst_name={formatting.hbold(user.first_name)}\n"
            )
            if quotes_time:
                set_send_time = formatting.hbold(str(quotes_time.set_send_time))
                last_send_time = formatting.hbold(str(quotes_time.last_send_time))
                msg = msg + (
                    f"Цитаты отправляем (время МСК):\n"
                    f"\t\t{set_send_time}\n"
                    f"Последняя отправка (время МСК):\n"
                    f"\t\t{last_send_time}"
                ),

            else:
                msg = msg + "В таблице нет данных по времени отправки цитат"

            bot.send_message(
                message.chat.id,
                text=msg
            )

        def return_main_menu_action():
            bot.send_message(message.chat.id, text="Вы вернулись в главное меню",
                             reply_markup=ButtonsMarkup.start_button_markup())

        actions = {
            Phrases.CONFIGURE_TEXT: config_bot_action,
            Phrases.QUOTES_SEND_TEXT: send_quote_action,
            Phrases.GET_BOT_CONFIG: bot_check_action,
            Phrases.RETURN_MAIN_MENY_TEXT: return_main_menu_action,
        }

        if message.text in actions:
            actions[message.text]()
        else:
            bot.send_message(
                message.chat.id,
                text='Не понимаю такую команду.',
            )


    try:
        bot.polling(none_stop=True)
    except requests.exceptions.ConnectionError as error:
        LogAssistant.put_to_log(logger=LOGGER, message=f'Возможно нет соединения с сетью. {error.args}',
                                with_print=True)
    except Exception:
        LogAssistant.put_to_log(logger=LOGGER, message=f'Неотловленная ошибка.',
                                with_print=True, with_trace=True)
