import csv
import os
import logging
from logging.handlers import RotatingFileHandler

import requests
from telegram import Bot, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater, Filters, MessageHandler

from dotenv import load_dotenv
from validators import validate_email, validate_password


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    filemode='a'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('my_logger.log', maxBytes=50000000, backupCount=2)
logger.addHandler(handler)

ASUS_BOT_TOKEN = os.getenv('ASUS_BOT_TOKEN', "")
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', "")

if not ASUS_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    logging.error('Бот не смог отправить сообщение')
    raise ValueError("Токен бота или пользователя не задан")

bot = Bot(token=ASUS_BOT_TOKEN)
updater = Updater(token=ASUS_BOT_TOKEN)

URL = 'https://api.thecatapi.com/v1/images/search'
URL_Y_N = 'https://yesno.wtf/api'
text = 'Для начала работы введите /start'


def say_hi(update, context):
    logging.info('say_hi')
    message = update.message.text
    chat = update.effective_chat
    text_mail = """
    Введите адрес вашей корпоративной почты и пароль разделенные пробелом
например:
ivanov@mariinsky.ru abcd1234
* Ваши данные будут храниться в зашифрованном виде"""
    if message == 'Войти в систему asus':
        context.bot.send_message(chat_id=chat.id, text=text_mail)
    else:
        context.bot.send_message(chat_id=chat.id, text='Не знаю что ответить на это :)')
    if (
        len(message.split()) == 2
        and validate_email(message.split()[0])
        and validate_password(message.split()[1])
    ):
        email = message.split()[0]
        password = message.split()[1]
        id = update.message.chat.id
        name = update.message.chat.first_name
        new_data = [str(id), name, email, password]
        with open("data.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if row == new_data:
                    context.bot.send_message(
                        chat_id=chat.id,
                        text='Вы уже регистрировали идентичные данные'
                    )
                    break
            else:
                with open("data.csv", "a", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(new_data)
                    print("Данные добавлены в data.csv!")
                    context.bot.send_message(
                        chat_id=chat.id,
                        text='Спасибо, данные верны и будут храниться в зашифрованном виде! Дальнейшая логика в разработке')


def wake_up(update, context):
    logging.info('wake_up')
    chat = update.effective_chat
    user = update.message.chat.first_name
    buttons = ReplyKeyboardMarkup([['/start', 'Войти в систему asus'],
                                  ['/newcat']], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text=f'{user}, спасибо что присодинился к асус-боту!',
        reply_markup=buttons
    )


def get_new_image():
    response = requests.get(URL).json()
    random_cat = response[0].get('url')
    return random_cat


# def yes_or_no():
#     response = requests.get(URL_Y_N).json()
#     random_answer = response.get('image')
#     return random_answer


def new_cat(update, context):
    logging.info('new_cat')
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())
    # context.bot.send_photo(chat.id, yes_or_no())


def main():
    bot.send_message(TELEGRAM_CHAT_ID, text)

    updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
