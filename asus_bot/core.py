import requests
from telegram import ReplyKeyboardMarkup

from constants import (BUTTONS, DAYS_TRACKING, HELP_MESSAGE, REGISTRATION_TEXT)
from db import (add_user, get_user, delete_user, update_day,
                add_schedule_to_db, get_schedule_from_db)
from logger_config import logger
from parsing import recieve_schedule, get_response
from validators import add_markdown, validate_password


def start(update, context):
    logger.info(f'start {update.message.chat.first_name}')
    chat_id = update.effective_chat.id
    user = update.message.chat.first_name
    context.bot.send_message(
        chat_id=chat_id,
        text=f"""<b>{user}</b>, привет!\n\nДобро пожаловать в асус-бот🤖!\n
Я умею отслеживать твоё недельное расписание и оперативно уведомлять об изменениях!\n
Помощь: /help
\n\n""",
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
    logger.info(f'registration() for{update.message.chat.first_name}')
    message = update.message.text
    chat_id = update.effective_chat.id
    if message == 'Войти в систему asus':
        context.bot.send_message(
            chat_id=chat_id, text=REGISTRATION_TEXT, parse_mode="HTML")
    if (
        len(message.split()) == 2
        and validate_password(message.split()[1])
        and check_registration(update, context)
    ):
        login = message.split()[0]
        password = message.split()[1]
        tg_id = update.message.chat.id
        name = update.message.chat.first_name
        if get_user(chat_id) is None:  #  changes here
            logger.info('get_user is None, trying to add to db')
            add_user(tg_id=tg_id, name=name, login=login,
                     password=password, days=DAYS_TRACKING, text='schedule')
            logger.info(f'sucsess regist. {update.message.chat.first_name}')
        else:
            logger.info('Double registration trying.')
            text = 'У вас уже есть asus-аккаунт, привязанный к ТГ'
            context.bot.send_message(chat_id=tg_id, text=text)


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
    logger.info(f'check_registration {update.message.chat.first_name}')
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='проверяем данные...')
    message = update.message.text
    email = message.split()[0]
    password = message.split()[1]
    response = get_response(email, password)
    if response:
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
    chat_id = user.tg_id
    if user.text == text:
        return True
    elif user.text != text:
        add_schedule_to_db(chat_id, text)
        return False


def delete_me(update, context):
    chat_id = update.effective_chat.id
    logger.info(f'delete_me for {update.message.chat.first_name}')
    user = get_user(chat_id)
    delete_user(user)


def get_logs(update, context):
    lines = 20
    words = update.message.text.split()
    if len(words) > 1 and words[1].isdigit():
        lines = int(words[1])
    chat_id = update.effective_chat.id
    logs = get_n_lines_logs("asus_bot_logger.log", lines)
    logs_text = "\n".join(logs)
    context.bot.send_message(chat_id=chat_id, text=logs_text)
    logger.info(f'message={update.message.text}, lines={lines}')


def get_n_lines_logs(filename, n):
    with open(filename, 'rb') as file:
        file.seek(0, 2)
        file_size = file.tell()
        buffer_size = 1024
        data = []
        lines_found = 0
        while file_size > 0 and lines_found < n:
            read_size = min(buffer_size, file_size)
            file_size -= read_size
            file.seek(file_size)
            buffer = file.read(read_size)
            data.append(buffer)
            lines_found = buffer.count(b'\n')
        all_data = b'\n'.join(reversed(data))
        last_lines = all_data.splitlines()[-n:]
        return [line.decode('utf-8', errors='ignore') for line in last_lines]


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
