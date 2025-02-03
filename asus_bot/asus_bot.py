import os
import time

from telegram import Bot
from telegram.ext import CommandHandler, Updater, Filters, MessageHandler

from core import days, new_cat, registration, start
from dotenv import load_dotenv
from logger_config import logger

load_dotenv()

ASUS_BOT_TOKEN = os.getenv('ASUS_BOT_TOKEN', "")
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', "")

if not ASUS_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    logger.error('Бот не смог отправить сообщение')
    raise ValueError("Токен бота или пользователя не задан")

bot = Bot(token=ASUS_BOT_TOKEN)
updater = Updater(token=ASUS_BOT_TOKEN)

start_text = 'Для начала работы нажмите /start'


def main():
    logger.info('main() starts')
    bot.send_message(TELEGRAM_CHAT_ID, start_text)

    updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('days_tracking', days))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, registration))

    updater.start_polling()
    updater.idle()


# if __name__ == '__main__':
#     main()
class HTTPError(Exception):
    """Пример кастомного исключения для теста (замени на реальную ошибку)."""
    pass


if __name__ == "__main__":
    while True:
        try:
            main()
            break  # Если main() успешно отработала, выходим из цикла
        except Exception as e:
            print(f"Ошибка: {e}. Повторный запуск через 2 секунды...")
            time.sleep(2)
