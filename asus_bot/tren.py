import threading
from datetime import datetime

import requests

pep_numbers = [1, 2, 4, 7, 8]


def task(num):
    response = requests.get(f'https://peps.python.org/pep-000{pep_numbers}/')
    response_html = response.text
    print(response_html[:50])
    print(f'Задача {num} выполнена.')


def sync_execute():
    tasks = []
    for num in pep_numbers:
        tasks.append(threading.Thread(target=task, args=(num,)))
    for t in tasks:
        t.start()
    for t in tasks:
        t.join()


if __name__ == '__main__':
    print('Последовательное выполнение кода:')
    start_time = datetime.now()
    sync_execute()
    end_time = datetime.now()
    print(f'Итоговое время выполнения: {end_time - start_time} секунд.')
