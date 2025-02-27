from dotenv import load_dotenv
import os

from bs4 import BeautifulSoup
import requests

from parsing_moscow import recieve_schedule

load_dotenv()

# print(recieve_schedule('I.yudin', 'Ps#up5i90$UL', 7))

TELEGRAM_TOKEN = os.getenv('ASUS_BOT_TOKEN', "")
LOGIN_URL_MSC = 'https://rep.mariinsky.ru/Account/Login'

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
print('Токен найден')
