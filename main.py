import os

import telebot
from dotenv import load_dotenv
from telebot import formatting, types

from app.services.app_logger import AppLogger
from app.services.ask_db import AskDB

load_dotenv('.env.dev')

LOGGER = AppLogger().get_logger()

if __name__ == '__main__':
    LOGGER.debug('Запускаем telebot')
    TOKEN = os.getenv('TOKEN')
    # bot = telebot.TeleBot(TOKEN)
    bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

    # Чтобы настроить меня нажми /configure .
    # А если ты нетерпелив, то жми /get_quote_now и я пришлю тебе одну цитату прямо сейчас.
    #  Я бот, который будет присылать тебе умную цитату в указанное тобой время. Надеюсь тебе понравиться.
    # {message.from_user.username}
    # {'' if message.from_user.username else formatting.hbold(message.from_user.username)}
    @bot.message_handler(commands=['start'])
    def start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Настроить")
        btn2 = types.KeyboardButton("Пришли цитату")
        markup.add(btn1, btn2)
        bot.send_message(
            message.chat.id,
            text="Привет.\nЯ бот, который будет присылать тебе умную цитату в указанное тобой время. Надеюсь тебе понравиться. \n",
            reply_markup=markup
        )

    # @bot.message_handler(commands=['configure'])
    # def start(message):
    #     bot.send_message(
    #         message.chat.id,
    #         text=f"""Конфигурировать пока не получится.""",
    #     )
    #
    #
    # @bot.message_handler(commands=['get_quote_now'])
    # def start(message):
    #     bot.send_message(
    #         message.chat.id,
    #         text=AskDB().random_quote(),
    #     )

    @bot.message_handler(content_types=['text'])
    def func(message):
        def config_bot():
            bot.send_message(
                message.chat.id,
                text="""В какое время по МСК присылать цитату? Формат HH:MM.""",
            )
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("07:00")
            btn2 = types.KeyboardButton("14:00")
            btn3 = types.KeyboardButton("14:00")
            markup.add(btn1, btn2, btn3)

        def get_quote_now():
            bot.send_message(
                message.chat.id,
                text=AskDB().random_quote(),
            )

        actions = {
            "Настроить": config_bot,
            "Пришли цитату": get_quote_now        }

        if message.text in actions:
            actions[message.text]()
        else:
            bot.send_message(
                message.chat.id,
                text='Не понимаю такую команду.',
            )

    bot.polling(none_stop=True)
