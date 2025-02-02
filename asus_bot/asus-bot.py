import os
import logging
from logging.handlers import RotatingFileHandler

from telegram import Bot
from telegram.ext import CommandHandler, Updater, Filters, MessageHandler

from core import days, new_cat, say_hi, start
from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    filemode='a'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(
    'my_logger.log', maxBytes=50000000, backupCount=2
)
logger.addHandler(handler)

ASUS_BOT_TOKEN = os.getenv('ASUS_BOT_TOKEN', "")
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', "")

if not ASUS_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    logging.error('Бот не смог отправить сообщение')
    raise ValueError("Токен бота или пользователя не задан")

bot = Bot(token=ASUS_BOT_TOKEN)
updater = Updater(token=ASUS_BOT_TOKEN)

start_text = 'Для начала работы нажмите /start'


def main():
    bot.send_message(TELEGRAM_CHAT_ID, start_text)

    updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('days_tracking', days))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
