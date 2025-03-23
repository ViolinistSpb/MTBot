import os
import time
import threading
from datetime import datetime

from telegram import Bot

from core import add_update_schedule
from db import get_all_users
from parsing import recieve_schedule

from dotenv import load_dotenv
from logger_config import logger
from validators import diff_func

load_dotenv()

ASUS_BOT_TOKEN = os.getenv('ASUS_BOT_TOKEN', "")
bot = Bot(token=ASUS_BOT_TOKEN)
UPDATE_INTERVAL = 900    # seconds
START_UPDATING_TIME = 9  # hours
END_UPDATING_TIME = 23   # hours
DAYS_TO_SEE = 7


def update_user(user):
    schedule = recieve_schedule(user.login, user.password, DAYS_TO_SEE)
    diff = diff_func(user.text, schedule)
    if add_update_schedule(schedule, user) is True:
        logger.info(f'NO UPD for {user.name}')
    else:
        logger.info(f'UPDATION for {user.name}')
        ALARM_TEXT = f"""
❗Ваше расписание изменилось:\n\n{diff}
Посмотреть расписание: /my_schedule"""
        logger.info(f'DIFF LENN: {len(diff)}')
        logger.debug(f'DIFF:\n{diff}')
        if new_day_flag is False and len(diff) > 30:
            logger.info(f'SEND NOTIF for {user.name}')
            bot.send_message(chat_id=user.tg_id, text=ALARM_TEXT)
        if new_day_flag is False and len(diff) <= 30:
            logger.info(f'NOT SEND SMALL DIFF for {user.name}')
        else:
            logger.info(f'1st SKIPPING for {user.name}')


def updation():
    logger.info('updation starts')
    tasks = []
    users = get_all_users()
    if users:
        logger.info(f'LEN USERS: {len(users)}')
        for user in users:
            tasks.append(threading.Thread(target=update_user, args=(user,)))
    for t in tasks:
        t.start()
    for t in tasks:
        t.join()


if __name__ == "__main__":
    count = 0
    now_hour = time.localtime().tm_hour
    new_day_flag = not (
        START_UPDATING_TIME <= now_hour <= END_UPDATING_TIME)
    while True:
        try:
            now_hour = time.localtime().tm_hour
            if START_UPDATING_TIME <= now_hour <= END_UPDATING_TIME:
                start_time = datetime.now()
                updation()
                end_time = datetime.now()
                logger.info(f'Working time: {end_time - start_time} sec.')
                if new_day_flag is True:
                    count += 1
                if new_day_flag is True and count < 2:
                    new_day_flag = True
                else:
                    new_day_flag = False
                    count = 0
                logger.info(f'new_day_flag = {new_day_flag}')
            else:
                logger.info('сон')
                new_day_flag = True
                logger.info('new_day_flag = True')
            time.sleep(UPDATE_INTERVAL)
        except Exception as e:
            logger.error(f'ERROR {e}')
            time.sleep(5)
