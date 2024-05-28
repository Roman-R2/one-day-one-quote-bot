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
from app.services.ask_db import AskDB
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
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("07:00")
        btn2 = types.KeyboardButton("08:00")
        btn3 = types.KeyboardButton("09:00")
        back = types.KeyboardButton(Phrases.RETURN_MAIN_MENY_TEXT)
        markup.add(btn1, btn2, btn3, back)
        return markup


if __name__ == '__main__':
    # Если быза данных не заполнена первичными данными, то сделаем это
    if FirstFillTables.get_quotes_table_row_count() < 1:
        print(f" Наполняем данными таблицу {Quotes.__name__}")
        FirstFillTables.fill_data()

    LogAssistant.put_to_log(logger=LOGGER, with_print=True,
                            message=f'Запускаем telebot\nPROD environment = {os.getenv("PROD")}')
    LOGGER.debug('Запускаем telebot')

    bot = telebot.TeleBot(settings.TOKEN, parse_mode="HTML")


    # Чтобы настроить меня нажми /configure .
    # А если ты нетерпелив, то жми /get_quote_now и я пришлю тебе одну цитату прямо сейчас.
    #  Я бот, который будет присылать тебе умную цитату в указанное тобой время. Надеюсь тебе понравиться.
    # {message.from_user.username}
    # {'' if message.from_user.username else formatting.hbold(message.from_user.username)}

    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(
            message.chat.id,
            text=f"Привет {message.from_user.first_name}.\nЯ бот, который будет присылать умную цитату в указанное время.\nРазмышляй, думай, учись.... \n",
            reply_markup=ButtonsMarkup.start_button_markup()
        )


    @bot.message_handler(content_types=['text'])
    def func(message):
        def config_bot_action():
            bot.send_message(
                message.chat.id,
                text="""Напишите, в какое время по МСК присылать вам цитату? Формат HH:MM.""",
                reply_markup=ButtonsMarkup.send_time_button_markup()
            )

        def send_quote_action():
            bot.send_message(
                message.chat.id,
                text=AskDB().random_quote(),
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
