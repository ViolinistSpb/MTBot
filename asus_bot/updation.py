import os
import time
import threading
from datetime import datetime

from telegram import Bot

from core import add_update_schedule
from db import get_all_users
from parsing_new import recieve_schedule

from dotenv import load_dotenv
from logger_config import logger
from validators import diff_func

load_dotenv()

ASUS_BOT_TOKEN = os.getenv('ASUS_BOT_TOKEN', "")
bot = Bot(token=ASUS_BOT_TOKEN)
UPDATE_INTERVAL = 600    # seconds
START_UPDATING_TIME = 9  # hours
END_UPDATING_TIME = 23   # hours


def update_user(user):
    # print(f'\n**\nработа с пользователем {user.name}')
    schedule = recieve_schedule(user.login, user.password, user.days)
    diff = diff_func(user.text, schedule)
    if add_update_schedule(schedule, user) is True:
        print(f'Обновление базы не потребовалось {user.name}')
        logger.info('updation() starts')
    else:
        print(f'Обновление расписания пользователя в базе {user.name}')
        ALARM_TEXT = f"""
❗Ваше расписание на {user.days} дн. изменилось:\n{diff}\n
Посмотреть расписание: /my_schedule"""
        if new_day_flag is False:
            print('Отправлено сообщение об изменении')
            bot.send_message(chat_id=user.tg_id, text=ALARM_TEXT)
        else:
            print('Не высылаю смену расписания утром')


def updation():
    logger.info('updation() starts')
    tasks = []
    users = get_all_users()
    if users:
        for user in users:
            tasks.append(threading.Thread(target=update_user, args=(user,)))
    for t in tasks:
        t.start()
    for t in tasks:
        t.join()
    print('sucsessfull finish updation func\n------------------------------\n')


if __name__ == "__main__":
    count = 1
    new_day_flag = False
    while True:
        try:
            now_hour = time.localtime().tm_hour
            print(time.asctime())
            if START_UPDATING_TIME <= now_hour <= END_UPDATING_TIME:
                start_time = datetime.now()
                updation()
                end_time = datetime.now()
                print(f'Время выполнения: {end_time - start_time} секунд.')
                new_day_flag = False
                time.sleep(UPDATE_INTERVAL)
                continue
            else:
                print('сон')
                new_day_flag = True
                time.sleep(UPDATE_INTERVAL)
                continue
        except Exception as e:
            print(f"Ошибка: {e}. Повторный запуск {count}/10 через 5 секунд")
            count += 1
            time.sleep(5)
