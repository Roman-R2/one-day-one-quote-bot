import datetime
import os
import time

import requests
import telebot
from dotenv import load_dotenv
from telebot import formatting, types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from app import settings
from app.models.models import Quotes
from app.services.app_logger import AppLogger
from app.services.database import DatabaseWork
from app.services.dq_queryes import DBQueryes
from app.services.dto import UserDTO
from app.services.first_fill_data import FirstFillTables
from app.services.log_assistant import LogAssistant

LOGGER = AppLogger().get_logger()


class Phrases:
    CONFIGURE_TEXT = "Настроить"
    QUOTES_SEND_TEXT = "Пришли цитату"
    RETURN_MAIN_MENY_TEXT = 'Вернуться в главное меню'


class ButtonsMarkup:
    @staticmethod
    def start_button_markup():
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(Phrases.CONFIGURE_TEXT)
        btn2 = types.KeyboardButton(Phrases.QUOTES_SEND_TEXT)
        markup.add(btn1, btn2)
        return markup

    @staticmethod
    def send_time_button_markup():
        markup = telebot.types.InlineKeyboardMarkup()
        btn1 = telebot.types.InlineKeyboardButton(text="07:00",
                                                  callback_data='assign_send_data-07:00')
        btn2 = telebot.types.InlineKeyboardButton(text="08:00",
                                                  callback_data='assign_send_data-08:00')
        btn3 = telebot.types.InlineKeyboardButton(text="09:00",
                                                  callback_data='assign_send_data-09:00')
        btn4 = telebot.types.InlineKeyboardButton(text="10:00",
                                                  callback_data='assign_send_data-10:00')
        btn5 = telebot.types.InlineKeyboardButton(text="11:00",
                                                  callback_data='assign_send_data-11:00')
        btn6 = telebot.types.InlineKeyboardButton(text="12:00",
                                                  callback_data='assign_send_data-12:00')
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        return markup


class GetData:
    @staticmethod
    def for_tg_user_data(message):
        # {'id': 232597319, 'is_bot': False, 'first_name': 'Roman Sl', 'username': 'Roman_R2Z',
        # 'last_name': None, 'language_code': 'ru', 'can_join_groups': None, 'can_read_all_group_messages': None,
        # 'supports_inline_queries': None, 'is_premium': None, 'added_to_attachment_menu': None, 'can_connect_to_business': None}`
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
        user_time = datetime.datetime.strptime(call.data.split('-')[1], '%H:%M')

        DBQueryes.save_quote_send_time(call, user_time)
        bot.send_message(
            call.message.chat.id,
            text=f"Установили время {user_time.strftime('%H:%M')}",
        )


    @bot.message_handler(commands=['start'])
    def start(message):
        # Возьмем или создадим пользовател в БД
        user: UserDTO = DBQueryes.current_user(message)
        bot.send_message(
            message.chat.id,
            text=f"Привет {formatting.hbold(user.username)}.\nЯ бот, который будет присылать умную цитату в указанное время.\nРазмышляй, думай, учись.... \n{user}",
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

        def return_main_menu_action():
            bot.send_message(message.chat.id, text="Вы вернулись в главное меню",
                             reply_markup=ButtonsMarkup.start_button_markup())

        actions = {
            Phrases.CONFIGURE_TEXT: config_bot_action,
            Phrases.QUOTES_SEND_TEXT: send_quote_action,
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
