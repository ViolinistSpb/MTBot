import threading
from datetime import datetime

import requests


def task(task_id):
    response = requests.get('https://python.org')
    response_html = response.text
    print(response_html[:15])
    print(f'Задача {task_id} выполнена.')


def sync_execute():
    tasks = []
    for i in range(1, 11):
        tasks.append(threading.Thread(target=task, args=(i,)))
        task(i)


if __name__ == '__main__':
    print('Последовательное выполнение кода:')
    start_time = datetime.now()
    sync_execute()
    end_time = datetime.now()
    print(f'Итоговое время выполнения: {end_time - start_time} секунд.')
