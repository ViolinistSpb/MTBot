import csv
import logging

from telegram import ReplyKeyboardMarkup
import requests

from validators import validate_email, validate_password


def start(update, context):
    logging.info('start')
    chat = update.effective_chat
    user = update.message.chat.first_name
    buttons = ReplyKeyboardMarkup([['/start', 'Войти в систему asus'],
                                  ['/days_tracking', '/newcat']],
                                  resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text=f'{user}, спасибо что присодинился к асус-боту!',
        reply_markup=buttons
    )


def days(update, context):
    print('days')
    chat = update.effective_chat
    buttons = ReplyKeyboardMarkup(
        [['/start', '/2', '/3'],
         ['/4', '/5', '/6', '/7']], resize_keyboard=True
    )
    context.bot.send_message(
        chat_id=chat.id,
        text='Выберите количество дней для отслеживания',
        reply_markup=buttons
    )


def get_new_image():
    URL = 'https://api.thecatapi.com/v1/images/search'
    response = requests.get(URL).json()
    random_cat = response[0].get('url')
    return random_cat


def new_cat(update, context):
    logging.info('new_cat')
    print(update.message.text)
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())


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
        context.bot.send_message(
            chat_id=chat.id, text='Не знаю что ответить на это :)'
        )
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
                with open("data.csv", "a",
                          newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(new_data)
                    print("Данные добавлены в data.csv!")
                    context.bot.send_message(
                        chat_id=chat.id,
                        text='Спасибо, данные верны и будут храниться'
                        'в зашифрованном виде!'
                        'Дальнейшая логика в разработке')
