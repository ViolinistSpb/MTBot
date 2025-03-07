# Импортируйте функцию из библиотеки.
from urllib.parse import urljoin
from dotenv import load_dotenv
import os

from bs4 import BeautifulSoup
import requests
import telegram

from constants import nums, maestros
from validators import add_markdown, clean_text


load_dotenv()

FORMAT = "%H:%M:%S"

# bot token
TELEGRAM_TOKEN = os.getenv('ASUS_BOT_TOKEN', "")

# user info
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
USERNAME = os.getenv('USERNAME')  # asus username
USERPASSWORD = os.getenv('USERPASSWORD')  # asus password
DAYS_TO_SEE = 7  # number of tracking days

LOGIN_URL = 'https://rep.mariinsky.ru/Account/Login'
LOGIN_URL_MSC = 'https://rep.bolshoi.ru/Account/Login'
SCHEDULE_URL = 'https://rep.mariinsky.ru/Home/Schedule'
REGISTRATION_URL = "https://rep.mariinsky.ru/Home/RegEmployee"
MAIN_URL = 'https://rep.mariinsky.ru/'

bot = telegram.Bot(token=TELEGRAM_TOKEN)


def find_place(session, surname, link):
    response = session.get(link)
    soup = BeautifulSoup(response.text, 'lxml')
    divs = soup.find_all('div', class_='color0')
    maestro = divs[0].text.strip()
    if len(maestro.split()) > 1:
        maestro = ''
    for div in divs:
        if surname in div.text:
            place = div.find('span').text
            if maestro != '' and maestro in (
                "Гергиев", "Кнапп", "Петросян", "Рылов", "Шупляков"
            ):
                maestro = 'дир. ' + maestro
            break
    return maestro, place  # Возвращает список кортежей (дирижер, место)


def get_response(username, password):
    session = requests.session()
    response = session.get(LOGIN_URL)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    token = soup.find(
        'input', attrs={'name': '__RequestVerificationToken'}
        )['value']
    if token is None:
        raise ValueError('Токен не найден')
    # print('Токен найден')
    data = {
        'username': username,
        'password': password,
        '__RequestVerificationToken': token
    }
    response = session.post(LOGIN_URL, data=data)
    response = session.get(SCHEDULE_URL)
    soup = BeautifulSoup(response.text, 'lxml')
    if soup.find('hgroup', attrs={'class': 'title'}):
        return False
    if soup.find('table', attrs={'class': 'table table-hover'}):
        return response, session
    else:
        return response, session


def recieve_schedule(username, password, days):
    response, session = get_response(username, password)
    soup = BeautifulSoup(response.text, 'lxml')
    # surname finding block
    li = soup.find('li', attrs={'id': 'menuLogin'})
    all_name = li.find('span').text.strip()
    surname = all_name.split()[0]
    # ---------------------
    table = soup.find('table', attrs={'class': 'table table-hover'})
    all_tr = table.find_all('tr')
    message_to_user = ''
    this_week = all_tr[1:8]
    for tr_one_day in this_week:
        tds_of_one_day = tr_one_day.find_all('td')
        DATE = tds_of_one_day[0].text.strip()
        message_to_user += f'{DATE}\n'
        all_rest_info = tds_of_one_day[1]
        all_divs = all_rest_info.find_all('div', attrs={'class': 'row'})
        for div in all_divs:
            all_fields = div.find_all('div', attrs={'class': 'col-md-2'})
            TIME = all_fields[0].text.strip()
            THEATRE = all_fields[1].text.strip()
            TYPE = all_fields[2].text.strip()
            PLAY = all_fields[3].text.strip()
            link = all_fields[2].find('a')
            if link:  # working day
                FULL_LINK = urljoin(MAIN_URL, link['href'])
                maestro, place = find_place(session, surname, FULL_LINK)
                event_message = (
                    f"{TIME}\n{THEATRE}, место {nums[place]}\n{PLAY}, {maestro}"
                )
            if link is None:  # free day
                event_message = (f'{TYPE}')
            message_to_user += f'{event_message}\n'
        message_to_user += '\n'
    return clean_text(message_to_user)
    # clean = clean_text(message_to_user)
    # bot.send_message(TELEGRAM_CHAT_ID, add_markdown(clean), parse_mode="HTML")

