import csv

from telegram import ReplyKeyboardMarkup
import requests

from validators import validate_email, validate_password
from logger_config import logger


def start(update, context):
    logger.info('start')
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
    logger.info('days')
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
    logger.info('new_cat')
    print(update.message.text)
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())


def registration(update, context):
    logger.info('registration')
    message = update.message.text
    chat = update.effective_chat
    text_registration = """
    Введите адрес вашей корпоративной почты и пароль разделенные пробелом
например:
ivanov@mariinsky.ru abcd1234
* Ваши данные будут храниться в зашифрованном виде"""
    if message == 'Войти в систему asus':
        context.bot.send_message(chat_id=chat.id, text=text_registration)
    if (
        len(message.split()) == 2
        and validate_email(message.split()[0])
        and validate_password(message.split()[1])
    ):
        email = message.split()[0]
        password = message.split()[1]
        id = update.message.chat.id
        name = update.message.chat.first_name
        new_row = [str(id), name, email, password]

        update_csv("data.csv", id, new_row, context)
        # with open("data.csv", "r", encoding="utf-8") as file:
        #     reader = csv.reader(file)
        #     for row in reader:
        #         if row == new_row:
        #             context.bot.send_message(
        #                 chat_id=chat.id,
        #                 text='Вы уже регистрировали идентичные данные'
        #             )
        #             logger.info('double registration trying')
        #             break
        #     else:
        #         with open("data.csv", "a",
        #                   newline="", encoding="utf-8") as file:
        #             writer = csv.writer(file)
        #             writer.writerow(new_row)
        #             logger.info('new data to data.csv')
        #             context.bot.send_message(
        #                 chat_id=chat.id,
        #                 text='Спасибо, данные верны и будут храниться'
        #                 'в зашифрованном виде!'
        #                 'Дальнейшая логика в разработке')


def update_csv(file_path, target_id, new_row, context):
    """Обновляет строку в CSV-файле по первому элементу (ID)."""

    rows = []
    found = False
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if row == new_row:
                context.bot.send_message(
                    chat_id=target_id,
                    text='Вы уже регистрировали идентичные данные'
                )
                logger.info('double registration trying')
                found = True
            elif row and int(row[0]) == target_id:  # Ищем нужную строку по первому элементу
                rows.append(new_row)  # Обновляем строку
                context.bot.send_message(
                    chat_id=target_id,
                    text='Спасибо, данные перезаписаны'
                    )
                logger.info('update registration')
                found = True
            else:
                rows.append(row)  # Оставляем без изменений
    if not found:
        rows.append(new_row)
        context.bot.send_message(
            chat_id=target_id,
            text=('Спасибо, данные верны и будут храниться '
                    'в зашифрованном виде! '
                    'Дальнейшая логика в разработке')
            )
        logger.info('new data has written')

    # Перезаписываем файл с обновлёнными данными
    with open(file_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)
        logger.info('file has rewritten')
