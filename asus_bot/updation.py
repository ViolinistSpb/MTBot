import os
import time

from telegram import Bot

from core import add_update_schedule
from db import get_all_users
from parsing_new import recieve_schedule

from dotenv import load_dotenv

load_dotenv()

ASUS_BOT_TOKEN = os.getenv('ASUS_BOT_TOKEN', "")
bot = Bot(token=ASUS_BOT_TOKEN)
UPDATE_INTERVAL = 600
START_UPDATING_TIME = 9
END_UPDATING_TIME = 23


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
                ALARM_TEXT = f"""
❗Ваше расписание на {user.days} дн. изменилось:\nПосмотреть: /my_schedule"""
                if new_day_flag is False:
                    bot.send_message(chat_id=user.tg_id, text=ALARM_TEXT)
                else:
                    print('Не высылаю смену расписания утром')
    print('sucsessfull finish updation func\n----------------- \n')


if __name__ == "__main__":
    count = 1
    while True:
        try:
            now_hour = time.localtime().tm_hour
            if START_UPDATING_TIME < now_hour < END_UPDATING_TIME:
                print(time.asctime())
                updation()
                new_day_flag = False
            else:
                print('сон')
                new_day_flag = True
            time.sleep(UPDATE_INTERVAL)
            continue
        except Exception as e:
            print(f"Ошибка: {e}. Повторный запуск {count}/10 через 5 секунд")
            count += 1
            time.sleep(5)
