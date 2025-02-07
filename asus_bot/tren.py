from bs4 import BeautifulSoup
import requests
import re

from parsing_new import dates_list


LOGIN_URL = 'https://rep.mariinsky.ru/Account/Login'
SCHEDULE_URL = 'https://rep.mariinsky.ru/Home/Schedule'


def recieve_schedule(username, password):
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
    table = soup.find('table', attrs={'class': 'table table-hover'})
    all_tr = table.find_all('tr')
    message = ''
    data = ''
    from_second_tr = all_tr[1:8]
    for tr in from_second_tr:
        div = tr.find('div').text
        message += '%'
        message += div
        div_internal = tr.find_all('div', attrs={'class': 'col-md-2'})
        for d in div_internal:
            message += " ".join(line.strip() for line in d.text.splitlines() if line.strip())
    list_message = message.split('%')
    final_message = ''
    for day in list_message:
        day = re.sub(r"(?<=[^\s])([А-Я])", r" \1", day)
        day = re.sub(r"(Оркестр)(?!\n)", r"\1\n", day)
        final_message += day
    return final_message


s = recieve_schedule('malkov@mariinsky.ru', '0t4=9x2E%1Yw')

print(s)
