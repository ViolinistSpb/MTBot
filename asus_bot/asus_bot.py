import os
import time

from telegram import Bot
from telegram.ext import CommandHandler, Updater, Filters, MessageHandler

from core import (days, new_cat, registration, start, my_schedule,
                  two, three, four, five, six, seven, my_info, help_handle)
from dotenv import load_dotenv
from logger_config import logger

load_dotenv()

ASUS_BOT_TOKEN = os.getenv('ASUS_BOT_TOKEN', "")

if not ASUS_BOT_TOKEN:
    logger.error('Бот не смог отправить сообщение')
    raise ValueError("Токен бота или пользователя не задан")

bot = Bot(token=ASUS_BOT_TOKEN)
updater = Updater(token=ASUS_BOT_TOKEN)


def main():
    logger.info('main() starts')
    updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help_handle))
    # updater.dispatcher.add_handler(CommandHandler('days', days))
    updater.dispatcher.add_handler(CommandHandler('my_info', my_info))
    updater.dispatcher.add_handler(CommandHandler('my_schedule', my_schedule))
    # updater.dispatcher.add_handler(CommandHandler('2', two))
    # updater.dispatcher.add_handler(CommandHandler('3', three))
    # updater.dispatcher.add_handler(CommandHandler('4', four))
    # updater.dispatcher.add_handler(CommandHandler('5', five))
    # updater.dispatcher.add_handler(CommandHandler('6', six))
    # updater.dispatcher.add_handler(CommandHandler('7', seven))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, registration))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    count = 1
    while True:
        try:
            print(time.asctime())
            main()
        except Exception as e:
            count += 1
            print(f"Ошибка: {e}. Повторный запуск {count}/10 через 5 секунд")
            time.sleep(5)
            continue
