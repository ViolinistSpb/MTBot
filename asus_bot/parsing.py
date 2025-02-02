from dotenv import load_dotenv
import os
import requests

import telegram
from bs4 import BeautifulSoup


load_dotenv()

FORMAT = "%H:%M:%S"

# bot token
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# user info
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
USERNAME = os.getenv('USERNAME')  # asus username
USERPASSWORD = os.getenv('USERPASSWORD')  # asus password
DAYS_TO_SEE = 2  # number of tracking days

RETRY_PERIOD = 60
LOGIN_URL = 'https://rep.mariinsky.ru/Account/Login'
SCHEDULE_URL = 'https://rep.mariinsky.ru/Home/Schedule'
REGISTRATION_URL = "https://rep.mariinsky.ru/Home/RegEmployee"
DATES = ['Послезавтра:', 'Завтра:', 'Сегодня:']

bot = telegram.Bot(token=TELEGRAM_TOKEN)


def send_message_to_user(message):
    """Sending message using bot."""
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    bot.send_message(TELEGRAM_CHAT_ID, message)


if __name__ == '__main__':
    session = requests.session()
    response = session.get(LOGIN_URL)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    token = soup.find('input',
                      attrs={'name': '__RequestVerificationToken'})['value']
    # print('token= ', token)
    if token is None:
        raise ValueError('Токен не найден')
    print('Токен найден')

    data = {
        'username': USERNAME,
        'password': USERPASSWORD,
        '__RequestVerificationToken': token
    }
    response = session.post(LOGIN_URL, data=data)
    response = session.get(SCHEDULE_URL)
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.find('table', attrs={'class': 'table table-hover'})
    all_tr = table.find_all('tr')
    second_tr = all_tr[1:(DAYS_TO_SEE+1)]
    message = ''
    for tr in second_tr:
        message += DATES.pop()
        all_div = tr.find_all('div')
        for d in all_div:
            div_internal = d.find_all('div', attrs={'class': 'col-md-2'})
            for div in div_internal:
                message += div.text
    message = ' '.join(message.split())
    message = message.replace('Первые скрипки', '\n')
    message = message.replace('Оркестр', '\n')

    # блок регистрации
    # time_now = datetime.now().strftime(FORMAT)
    # data = {
    #     "regAlert": "",
    #     "regText": "Успешная регистрация",
        # "regTime": "Время регистрации: " + time_now
        # }
    
    # body = {'body': 'regAlert=&regText=%D0%A3%D1%81%D0%BF%D0%B5%D1%88%D0%BD%D0%B0%D1%8F+%D1%80%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F&regTime=%D0%92%D1%80%D0%B5%D0%BC%D1%8F+%D1%80%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D0%B8%3A+18%3A45%3A22'}

    # response = session.post(REGISTRATION_URL, data=data)
    # print(response.status_code)
    # soup = BeautifulSoup(response.text, 'lxml')
    # print(soup.text)
    # print(response.headers)
    # print(requests)
    # pprint(response.request.__dict__)
    # pprint(response.request.body)

    # отправка уведомления
    print(message)
    send_message_to_user(message)
    print("Сообщение отправлено пользователю")
