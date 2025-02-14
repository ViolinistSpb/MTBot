from telegram import ReplyKeyboardMarkup


DAYS_TRACKING = 3
FILE_PATH = "data.csv"

BUTTONS = ReplyKeyboardMarkup(
    [['/start', 'Войти в систему asus'],
     ['/my_info', '/my_schedule'],
     ['/days', '/newcat', '/help']],
    resize_keyboard=True)

HELP_MESSAGE = """Команды:
⚪ /start – Вернуться к началу
⚪ /Войти в систему asus – Ввести данные для авторизации
⚪ /my_info – Получить свои данные
⚪ /my_schedule – Получить свое расписание
⚪ /days_tracking – Выбрать количество дней для отслеживания
⚪ /newcat – Получить котика 🐈‍⬛️
⚪ /help – Показать доступные команды
"""

REGISTRATION_TEXT = """
Введите адрес вашей корпоративной почты (или логин) и через пробел пароль
например:
ivanov abcd1234
ivanov@mariinsky.ru abcd1234
* Ваши данные будут храниться в зашифрованном виде"""
