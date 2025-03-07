import os
from datetime import datetime

from dotenv import load_dotenv

from parsing import recieve_schedule

load_dotenv()

ASUS_BOT_TOKEN = os.getenv('ASUS_BOT_TOKEN', "")
LOGIN_URL = 'https://rep.mariinsky.ru/Account/Login'
SCHEDULE_URL = 'https://rep.mariinsky.ru/Home/Schedule'
MAIN_URL = 'https://rep.mariinsky.ru/'
chat_id = '1054725325'

TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
# USERNAME = os.getenv('USERNAME')  # asus username
# USERPASSWORD = os.getenv('USERPASSWORD')  # asus password

USERNAME = 'lan'
USERPASSWORD = 'vitaly_pugachev13.11.1989'
DAYS_TO_SEE = 7

start_time = datetime.now()
recieve_schedule(USERNAME, USERPASSWORD, DAYS_TO_SEE)
end_time = datetime.now()
print(f'Working time: {end_time - start_time} sec.')
