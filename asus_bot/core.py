import requests
from telegram import ReplyKeyboardMarkup

from constants import (BUTTONS, DAYS_TRACKING, HELP_MESSAGE, REGISTRATION_TEXT)
from db import (add_user, get_user, update_day,
                add_schedule_to_db, get_schedule_from_db)
from logger_config import logger
from parsing_new import recieve_schedule, get_response
from validators import add_markdown, validate_password


def start(update, context):
    logger.info(f'start {update.message.chat.first_name}')
    chat_id = update.effective_chat.id
    user = update.message.chat.first_name
    context.bot.send_message(
        chat_id=chat_id,
        text=f'<b>{user}</b>, привет!\nСпасибо что присоединился к асус-боту!'
             f'🤖\n\n',
        reply_markup=BUTTONS,
        parse_mode="HTML")


def help_handle(update, context):
    logger.info(f'help {update.message.chat.first_name}')
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=HELP_MESSAGE,
        reply_markup=BUTTONS)


def days(update, context):
    logger.info(f'days {update.message.chat.first_name}')
    chat_id = update.effective_chat.id
    buttons = ReplyKeyboardMarkup(
        [['/start', '/2', '/3'],
         ['/4', '/5', '/6', '/7']], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat_id,
        text='Выберите количество дней для отслеживания',
        reply_markup=buttons)


def registration(update, context):
    print('registration func')
    logger.info(f'registration {update.message.chat.first_name}')
    message = update.message.text
    chat_id = update.effective_chat.id
    if message == 'Войти в систему asus':
        context.bot.send_message(chat_id=chat_id, text=REGISTRATION_TEXT)
    if (
        len(message.split()) == 2
        and validate_password(message.split()[1])
        and check_registration(update, context)
    ):
        print('all valid')
        login = message.split()[0]
        password = message.split()[1]
        tg_id = update.message.chat.id
        name = update.message.chat.first_name
        add_user(tg_id=tg_id, name=name, login=login,
                 password=password, days=DAYS_TRACKING)
        logger.info(f'sucsess registration {update.message.chat.first_name}')


def my_info(update, context):
    print('my_info func')
    logger.info(f'my_info {update.message.chat.first_name}')
    chat_id = update.effective_chat.id
    user = get_user(chat_id)
    if user:
        text = (f'Ваш Телеграм ID: {user.tg_id}\n'
                f'Ваше Имя в Телеграм: {user.name}\n'
                f'Почта: {user.login}\n'
                f'Пароль: {user.password}\n'
                f'Количество дней отслеживания: {user.days}')
        context.bot.send_message(chat_id, text=text)


def my_schedule(update, context):
    print('my_schedule func')
    logger.info(f'my_schedule {update.message.chat.first_name}')
    chat_id = update.effective_chat.id
    schedule_from_db = get_schedule_from_db(chat_id)
    if schedule_from_db is None:
        context.bot.send_message(chat_id, text='несколько секунд...')
        user = get_user(chat_id)
        text = recieve_schedule(user.login, user.password, user.days)
        logger.info(f'get data from site {update.message.chat.first_name}')
        add_update_schedule(text, user)
    if schedule_from_db is not None:
        text = schedule_from_db
        logger.info(f'get data from db {update.message.chat.first_name}')
    text = add_markdown(text)
    context.bot.send_message(chat_id, text=text, parse_mode="HTML")


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


def add_update_schedule(text, user):
    logger.info(f'add_schedule_to_db {user.name}')
    print("add_update_schedule")
    chat_id = user.tg_id
    if user.text == text:
        print('то же расписание')
        return True

    elif user.text != text:
        print('новое расписание')
        add_schedule_to_db(chat_id, text)
        return False


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


def get_new_image():
    URL = 'https://api.thecatapi.com/v1/images/search'
    response = requests.get(URL).json()
    random_cat = response[0].get('url')
    return random_cat


def new_cat(update, context):
    logger.info(f'new_cat {update.message.chat.first_name}')
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id, get_new_image())
