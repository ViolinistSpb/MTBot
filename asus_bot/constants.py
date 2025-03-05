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

🔐 Ваши данные будут храниться в зашифрованном виде"""

nums = {
    '1': '1️⃣',
    '2': '2️⃣',
    '3': '3️⃣',
    '4': '4️⃣',
    '5': '5️⃣',
    '6': '6️⃣',
    '7': '7️⃣',
    '8': '8️⃣',
    '10': '🔟',
    '11': '1️⃣1️⃣',
    '12': '1️⃣2️⃣',
    '13': '1️⃣3️⃣',
    '14': '1️⃣4️⃣'
}