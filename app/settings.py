import logging
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# load_dotenv(BASE_DIR / '.env')
#
is_prod = True if os.getenv('PROD', '0') == '1' else False
if not is_prod:
    load_dotenv(BASE_DIR / '.env.dev')

# Telegram bot token
TOKEN = os.environ.get('TOKEN')

# DB environments
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Logging configuration
APP_LOGGING_LEVEL = logging.DEBUG
APP_LOG_FOLDER = BASE_DIR / 'logs'
APP_LOG_FILE = APP_LOG_FOLDER / 'quotes_bot.log'
APP_LOGGER_NAME = 'quotes_bot_logger'
