import csv

from telegram import ReplyKeyboardMarkup
import requests

from validators import validate_email, validate_password
from logger_config import logger

from db import add_user, update_day
from parsing_new import recieve_schedule, get_response
from validators import clean_day, pre_clean_day
from constants import (BUTTONS, DAYS_TRACKING, HELP_MESSAGE,
                       FILE_PATH, REGISTRATION_TEXT)


def start(update, context):
    logger.info(f'start {update.message.chat.first_name}')
    chat = update.effective_chat
    user = update.message.chat.first_name
    context.bot.send_message(
        chat_id=chat.id,
        text=f'<b>{user}</b>, привет!\nСпасибо что присоединился к асус-боту! 🤖\n\n',
        reply_markup=BUTTONS,
        parse_mode="HTML"
    )


def help_handle(update, context):
    logger.info(f'help {update.message.chat.first_name}')
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=HELP_MESSAGE,
        reply_markup=BUTTONS)


def days(update, context):
    logger.info(f'days {update.message.chat.first_name}')
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
    logger.info(f'new_cat {update.message.chat.first_name}')
    print(update.message.text)
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())


def registration(update, context):
    print('registration func')
    logger.info(f'registration {update.message.chat.first_name}')
    message = update.message.text
    chat = update.effective_chat
    if message == 'Войти в систему asus':
        context.bot.send_message(chat_id=chat.id, text=REGISTRATION_TEXT)
    elif (
        len(message.split()) == 2
        and validate_password(message.split()[1])
        and check_registration(update, context)
    ):
        print('all valid')
        login = message.split()[0]
        password = message.split()[1]
        id = update.message.chat.id
        name = update.message.chat.first_name
        add_user(tg_id=id, name=name, login=login,
                 password=password, days=DAYS_TRACKING)
        logger.info(f'sucsess registration {update.message.chat.first_name}')


def update_csv(target_id, new_row, context, update):
    """Обновляет или добавляет строку в CSV-файле по первому элементу."""

    rows = []
    found = False
    with open(FILE_PATH, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if row == new_row:
                context.bot.send_message(
                    chat_id=target_id,
                    text='Вы уже регистрировали идентичные данные')
                logger.info(
                    f'double registration {update.message.chat.first_name}')
                rows.append(row)
                found = True
            elif row and int(row[0]) == target_id:  # Ищем нужную строку
                rows.append(new_row)  # Обновляем строку
                context.bot.send_message(
                    chat_id=target_id,
                    text='Спасибо, данные перезаписаны'
                    )
                logger.info(
                    f'update registration {update.message.chat.first_name}')
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
        logger.info(f'new data has written {update.message.chat.first_name}')

    # Перезаписываем файл с обновлёнными данными
    with open(FILE_PATH, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)
        logger.info(f'file has rewritten {update.message.chat.first_name}')


def update_day_csv(target_id, new_day, context, update):
    print('updateday')
    logger.info(f'update_day_csv {update.message.chat.first_name}')
    """Обновляет дни в CSV-файле в поиске по первому элементу."""
    rows = []
    with open(FILE_PATH, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if row and isinstance(int(row[0]), int) and int(row[0]) == target_id:
                print('found me')
                if len(row) == 6:
                    print('len=6')
                    new_row = row[:4] + [new_day] + [row[-1]]
                    print(new_row)
                if len(row) == 5 or len(row) == 4:
                    print(f'len={len(row)}')
                    new_row = row[:4] + [new_day]
                    print(new_row)
                rows.append(new_row)
            else:
                print('else')
                rows.append(row)
    with open(FILE_PATH, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)
        logger.info(f'Days has changed {update.message.chat.first_name}')


def my_info(update, context):
    logger.info(f'my_info {update.message.chat.first_name}')
    with open('data.csv', mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if row and int(row[0]) == update.effective_chat.id:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=(f'Ваш Телеграм ID: {row[0]}\n'
                          f'Имя в Телеграм: {row[1]}\n'
                          f'Почта:{row[2]}\n'
                          f'Пароль:{row[3]}\n'
                          f'Количество дней отслеживания:{row[4]}'))


def my_schedule(update, context):
    logger.info(f'my_schedule {update.message.chat.first_name}')
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='несколько секунд...')
    with open('data.csv', mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if row and isinstance(int(row[0]), int) and int(row[0]) == update.effective_chat.id:
                email = row[2]
                password = row[3]
                days = row[4]
                raw_text = recieve_schedule(email, password, days)
                text_for_csv = pre_clean_day(raw_text)
                clear_text = clean_day(text_for_csv)
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=clear_text,
                    parse_mode="HTML")
                logger.info(f'data received {update.message.chat.first_name}')
                # add_schedule_to_csv(text_for_csv, update, context)


def check_registration(update, context):
    print('check_registration func')
    logger.info(f'check_registration {update.message.chat.first_name}')
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='проверяем данные...')
    message = update.message.text
    email = message.split()[0]
    password = message.split()[1]
    response = get_response(email, password)
    if response:
        print('status: 200')
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Удачная регистрация!')
        logger.info(f'correct registration {update.message.chat.first_name}')
        return True
    print('status NOT 200')
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Регистрация не удалась, проверьте данные!')
    logger.info(f'bad registration trying {update.message.chat.first_name}')
    return False


def add_schedule_to_csv(text, update, context):
    logger.info(f'add_schedule_to_csv {update.message.chat.first_name}')
    print("add_schedule_to_csv")
    """Добавляет текст в CSV-файл в поиске по первому элементу."""
    rows = []
    with open(FILE_PATH, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)
            if row and int(row[0]) == update.effective_chat.id:
                if len(row) == 5:
                    print('len=5')
                    new_row = row.append(text)
                if len(row) == 6:
                    print('len=5')
                    if row[5] == text:
                    #  отправить уведомление
                    # print('отправить уведомление')
                    # notification(update, context)
                    # my_schedule(update, context)
                        rows.append(row)
                        print('текст тот же')
                    else:
                        print('текст другой')
                        new_row = row[:5] + [text]
                        rows.append(new_row)
            else:
                rows.append(row)
    with open(FILE_PATH, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)
        logger.info(f'Schedule has changed {update.message.chat.first_name}')


def notification(update, context):
    print('notification')
    logger.info(f'notification {update.message.chat.first_name}')
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='В расписании произошли изменения!')


def bot_send_day_message(context, update, new_days):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Вы выбрали {new_days} дней для отслеживания',
        reply_markup=BUTTONS
    )


def two(update, context):
    logger.info(f'two {update.message.chat.first_name}')
    new_days = 2
    update_day(update.effective_chat.id, new_days)
    bot_send_day_message(context, update, new_days)


def three(update, context):
    logger.info(f'three {update.message.chat.first_name}')
    new_days = 3
    update_day(update.effective_chat.id, new_days)
    bot_send_day_message(context, update, new_days)


def four(update, context):
    logger.info(f'four {update.message.chat.first_name}')
    new_days = 4
    update_day(update.effective_chat.id, new_days)
    bot_send_day_message(context, update, new_days)


def five(update, context):
    logger.info(f'five {update.message.chat.first_name}')
    new_days = 5
    update_day(update.effective_chat.id, new_days)
    bot_send_day_message(context, update, new_days)


def six(update, context):
    logger.info(f'six {update.message.chat.first_name}')
    new_days = 6
    update_day(update.effective_chat.id, new_days)
    bot_send_day_message(context, update, new_days)


def seven(update, context):
    logger.info(f'seven {update.message.chat.first_name}')
    new_days = 7
    update_day(update.effective_chat.id, new_days)
    bot_send_day_message(context, update, new_days)
