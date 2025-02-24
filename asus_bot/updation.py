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
    logger.info(f'work with {user.name}')
    schedule = recieve_schedule(user.login, user.password, user.days)
    diff = diff_func(user.text, schedule)
    if add_update_schedule(schedule, user) is True:
        logger.info(f'NO UPD for {user.name}')
    else:
        logger.info(f'UPDATION for {user.name}')
#         ALARM_TEXT = """
# ❗Ваше расписание изменилось:\n
# Посмотреть расписание: /my_schedule"""
        ALARM_TEXT = f"""
❗Ваше расписание изменилось:\n{diff}\n
Посмотреть расписание: /my_schedule"""
        if new_day_flag is False and len(diff) > 20:
            logger.info(f'SEND NOTIF for {user.name}')
            logger.debug(f'DIFF: {diff}\nOLD_SCHEDULE: {user.text}\nNEW_SCHEDULE: {schedule}\n for {user.name}')
            bot.send_message(chat_id=user.tg_id, text=ALARM_TEXT)
        else:
            logger.info(f'1st message SKIPPING {user.name}')


def updation():
    logger.info('updation starts')
    tasks = []
    users = get_all_users()
    if users:
        for user in users:
            tasks.append(threading.Thread(target=update_user, args=(user,)))
    for t in tasks:
        t.start()
    for t in tasks:
        t.join()


if __name__ == "__main__":
    count = 1
    new_day_flag = True
    while True:
        try:
            now_hour = time.localtime().tm_hour
            print(f'start updating {time.asctime()}')
            if START_UPDATING_TIME <= now_hour <= END_UPDATING_TIME:
                start_time = datetime.now()
                updation()
                end_time = datetime.now()
                logger.info(f'Время выполнения: {end_time - start_time} секунд.')
                logger.info('sucsessfull finish updation func\n------------------------------\n')
                new_day_flag = False
                logger.info('new_day_flag = False')
            else:
                logger.info('сон')
                new_day_flag = True
                logger.info('new_day_flag = True')
            time.sleep(UPDATE_INTERVAL)
        except Exception as e:
            print(f"Ошибка: {e}. Повторный запуск {count}/10 через 5 секунд")
            count += 1
            time.sleep(5)
