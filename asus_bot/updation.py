import time

from core import add_update_schedule
from db import get_all_users
from parsing_new import recieve_schedule


def updation():
    print('updation func')
    users = get_all_users()
    if users:
        for user in users:
            schedule = recieve_schedule(user.login, user.password, user.days)
            add_update_schedule(schedule, user)
    print('sucsessfull finish updation func')


if __name__ == "__main__":
    count = 2
    while True:
        try:
            print(time.asctime())
            updation()
            time.sleep(600)
            continue
        except Exception as e:
            print(f"Ошибка: {e}. Повторный запуск {count}/10 через 5 секунд")
            count += 1
            time.sleep(5)
