from urllib.parse import urljoin
from dotenv import load_dotenv
import os

from bs4 import BeautifulSoup
import requests
import telegram

from validators import clean_text


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


def recieve_schedule(username, password, days):   # add session
    response, session = get_response(username, password)   # add session
    soup = BeautifulSoup(response.text, 'lxml')
    # surname finding block
    li = soup.find('li', attrs={'id': 'menuLogin'})
    all_name = li.find('span').text.strip()
    surname = all_name.split()[0]
    # ---------------------
    table = soup.find('table', attrs={'class': 'table table-hover'})
    all_tr = table.find_all('tr')
    message = ''
    links_list = []  # инициализация списка ссылок
    from_second_tr = all_tr[1:8]
    for tr in from_second_tr:
        td = tr.find_all('td')[1]
        links = td.find_all('a')
        if links:  # если есть ссылки, добавляем их в список
            for link in links:
                links_list.append(urljoin(MAIN_URL, link['href']))
        div = tr.find('div').text
        message += '%'
        message += div
        div_internal = tr.find_all('div', attrs={'class': 'col-md-2'})
        for d in div_internal:
            message += " ".join(
                line.strip() for line in d.text.splitlines() if line.strip())
    list_message = message.split('%')
    list_message = list_message[:1+int(days)]
    final_message = ''
    # for day in list_message:
    #     final_message += day
    places = find_place(session, surname, links_list)  # отправляем в функцию парсинга мест
    print(f'len(places): {len(places)}')
    print(f'len(list_message): {len(list_message)}')
    print(places)
    for i in range(len(list_message)):
        print(list_message[i], i)
        final_message += list_message[i]
        try:
            print(places[i])
            if 'Выходной' not in list_message[i].split():
                if isinstance(places[i], tuple):
                    final_message += ", ".join(places[i])
                if isinstance(places[i], str):
                    final_message += places[i]
        except IndexError:
            None
    return clean_text(final_message)


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
        return response, session  # add session
    else:
        return response, session  # add session


def find_place(session, surname, links_list):
    places = []
    for link in links_list:
        response = session.get(link)
        soup = BeautifulSoup(response.text, 'lxml')
        divs = soup.find_all('div', class_='color0')
        maestro = divs[0].text.strip()
        if len(maestro.split()) > 1:
            maestro = ''
        for div in divs:
            if surname in div.text:
                place = div.find('span').text + ' место'
                if maestro != '':
                    maestro = 'Дир. ' + maestro
                    places.append((maestro, place))
                else:
                    places.append(place)
                break
    return places  # Возвращает список кортежей (дирижер, место пользователя)
