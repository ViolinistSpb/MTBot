import os

from dotenv import load_dotenv

from parsing_new import recieve_schedule

load_dotenv()

ASUS_BOT_TOKEN = os.getenv('ASUS_BOT_TOKEN', "")
LOGIN_URL = 'https://rep.mariinsky.ru/Account/Login'
SCHEDULE_URL = 'https://rep.mariinsky.ru/Home/Schedule'
MAIN_URL = 'https://rep.mariinsky.ru/'
chat_id = '1054725325'

TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
USERNAME = os.getenv('USERNAME')  # asus username
USERPASSWORD = os.getenv('USERPASSWORD')  # asus password
DAYS_TO_SEE = 7


recieve_schedule