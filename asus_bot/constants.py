from telegram import ReplyKeyboardMarkup


DAYS_TRACKING = 7
FILE_PATH = "data.csv"

BUTTONS = ReplyKeyboardMarkup(
    [['/start', 'Войти в систему asus'],
     ['/my_info', '/my_schedule'],
     ['/newcat', '/help']],
    resize_keyboard=True)

HELP_MESSAGE = """Команды:
⚪ /start – Вернуться к началу
⚪ /Войти в систему asus – Ввести данные для авторизации
⚪ /my_info – Получить свои данные
⚪ /my_schedule – Получить свое расписание
⚪ /newcat – Получить котика 🐈‍⬛️
⚪ /help – Показать доступные команды
"""
#  ⚪ /days_tracking – Выбрать количество дней для отслеживания

REGISTRATION_TEXT = """
Введите логин или почту
и <b>через пробел</b> пароль

<i>например</i>:
ivanov@mariinsky.ru abcd1234

* Ваши данные будут храниться в зашифрованном виде"""
