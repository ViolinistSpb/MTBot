from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests
import telegram


load_dotenv()

FORMAT = "%H:%M:%S"

# bot token
TELEGRAM_TOKEN = os.getenv('ASUS_BOT_TOKEN', "")

# user info
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
USERNAME = os.getenv('USERNAME')  # asus username
USERPASSWORD = os.getenv('USERPASSWORD')  # asus password
DAYS_TO_SEE = 2  # number of tracking days

LOGIN_URL = 'https://rep.mariinsky.ru/Account/Login'
SCHEDULE_URL = 'https://rep.mariinsky.ru/Home/Schedule'
REGISTRATION_URL = "https://rep.mariinsky.ru/Home/RegEmployee"
MAIN_URL = 'https://rep.mariinsky.ru/'

bot = telegram.Bot(token=TELEGRAM_TOKEN)


def recieve_schedule(username, password, days):
    response = get_response(username, password)
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.find('table', attrs={'class': 'table table-hover'})
    all_tr = table.find_all('tr')
    message = ''
    from_second_tr = all_tr[1:8]
    for tr in from_second_tr:
        div = tr.find('div').text
        message += '%'
        message += div
        div_internal = tr.find_all('div', attrs={'class': 'col-md-2'})
        for d in div_internal:
            href = d.find('a')
            if href is not None:
                href = urljoin(MAIN_URL, href["href"])
                print(href)
            message += " ".join(line.strip() for line in d.text.splitlines() if line.strip())
    list_message = message.split('%')
    final_message = ''
    for day in list_message[:1+int(days)]:
        day = re.sub(r"(?<=[^\s])([А-Я])", r" \1", day)
        day = re.sub(r"(Оркестр)(?!\n)", r"\1\n", day)
        # day = re.sub(r"\d{2}:\d{2} - \d{2}:\d{2}", r"<b>\1</b>", day)
        # day = re.sub(r")М\d", r"<b>\1</b>", day) <b><i>Жирный курсив</i></b>
        pattern = r"([А-Я][а-я]) (\d{2}\.\d{2}\.\d{4})"  #  жирный шрифт к дате
        day = re.sub(pattern, r"<b>\1 \2</b>", day)
        pattern = r"(\d{2}:\d{2})( - )(\d{2}:\d{2})"  #  жирный шрифт ко времени
        day = re.sub(pattern, r"<i>\1 \2 \3</i>", day)
        pattern = r"([MМ][123])"  #  жирный шрифт ко времени
        day = re.sub(pattern, r"<b><i>\1</i></b>", day)
        words_to_remove = ["Первые скрипки", "Вторые скрипки", "Альты", "Оркестр"]
        for word in words_to_remove:
            day = day.replace(word, "")
        final_message += day
    if final_message is not None:
        print('Данные отправлены')
    return final_message


def get_response(username, password):
    print('get_response func')
    session = requests.session()
    response = session.get(LOGIN_URL)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    token = soup.find('input', attrs={'name': '__RequestVerificationToken'})['value']
    if token is None:
        raise ValueError('Токен не найден')
    print('Токен найден')
    data = {
        'username': username,
        'password': password,
        '__RequestVerificationToken': token
    }
    response = session.post(LOGIN_URL, data=data)
    response = session.get(SCHEDULE_URL)
    soup = BeautifulSoup(response.text, 'lxml')
    if soup.find('hgroup', attrs={'class': 'title'}):
        print('hgroup div found')
        return False
    if soup.find('table', attrs={'class': 'table table-hover'}):
        print('table  found')
        print('GOOD')
        return response
    else:
        print('else')
        return response
