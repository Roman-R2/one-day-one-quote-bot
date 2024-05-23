import logging
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env.dev')

DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# -------------- Настройки логирования
# Уровень логирования
APP_LOGGING_LEVEL = logging.DEBUG
# Папка логов
APP_LOG_FOLDER = BASE_DIR / 'logs'
# Файл логов
APP_LOG_FILE = APP_LOG_FOLDER / 'quotes_bot.log'
# Имя логера для создания бэкапов
APP_LOGGER_NAME = 'quotes_bot_logger'
