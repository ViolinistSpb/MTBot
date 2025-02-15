import time

from core import add_update_schedule
from db import get_all_users
from parsing_new import recieve_schedule

import os

from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

ASUS_BOT_TOKEN = os.getenv('ASUS_BOT_TOKEN', "")
bot = Bot(token=ASUS_BOT_TOKEN)
UPDATE_INETRVAL = 600
NOTIFICATION_TEXT = '❗Ваше расписание на выбраное количество дней изменилось:\n/my_schedule'


def updation():
    print('updation func')
    users = get_all_users()
    if users:
        for user in users:
            print(f'\n**\nработа с пользователем {user.id}')
            schedule = recieve_schedule(user.login, user.password, user.days)
            if add_update_schedule(schedule, user) is True:
                print('Обновление базы не потребовалось')
            else:
                print('Обновление расписания пользователя в базе')
                bot.send_message(chat_id=user.tg_id, text=NOTIFICATION_TEXT)
    print('sucsessfull finish updation func\n----------------- \n')


if __name__ == "__main__":
    count = 2
    while True:
        try:
            print(time.asctime())
            updation()
            time.sleep(UPDATE_INETRVAL)
            continue
        except Exception as e:
            print(f"Ошибка: {e}. Повторный запуск {count}/10 через 5 секунд")
            count += 1
            time.sleep(5)
