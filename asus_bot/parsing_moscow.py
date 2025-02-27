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


def recieve_schedule(username, password, days):
    response = get_response(username, password)
    soup = BeautifulSoup(response.text, 'lxml')
    # surname finding block
    li = soup.find('li', attrs={'id': 'menuLogin'})
    all_name = li.find('span').text.strip()
    surname = all_name.split()[0]
    # ---------------------
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
            message += " ".join(
                line.strip() for line in d.text.splitlines() if line.strip())
    list_message = message.split('%')
    final_message = ''
    for day in list_message[:1+int(days)]:
        final_message += day
    return clean_text(final_message), surname


def get_response(username, password):
    print('get_response()')
    session = requests.session()
    response = session.get(LOGIN_URL_MSC)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    print(soup)
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
    response = session.post(LOGIN_URL_MSC, data=data)
    response = session.get(SCHEDULE_URL)
    soup = BeautifulSoup(response.text, 'lxml')
    if soup.find('hgroup', attrs={'class': 'title'}):
        return False
    if soup.find('table', attrs={'class': 'table table-hover'}):
        return response
    else:
        return response
