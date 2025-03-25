[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-360/)
<br/><br/>

<div align="center">
  <h1 align="center">Бот информирования о рабочем расписании
  </h1>
</div>


## Цели и задачи проекта

<h4>
  
* Разработка телеграм-бота, осуществляющего контроль за индивидуальным расписанием сотрудника,
    включая уведомления о его изменении.
  
</h4>

## Используемый стек и технологии

- [Python 3.11](https://docs.python.org/3.11/)
- [Beautifulsoup4 4.12.3](https://pypi.org/project/beautifulsoup4/)
- [Python-telegram-bot](https://pypi.org/project/python-telegram-bot/)
- [SQlite](https://www.sqlite.org/)
- [SQLAlchemy 2.0.21](https://www.sqlalchemy.org/)

## Структура и назначение папок и файлов проекта

### /asus_bot - Папка с кодом проекта

* **asus_bot.py**  - файл запуска бота, сканирование входящих сообщений

* **constants.py**  - файл переменных

* **core.py** - основной файл хендлеров и вспомогательных функций

* **db.py** - файл настроек базы данных и функций для взаимодействия с ней

* **.env.example** - пример файла с переменными окружения

* **diff_match_pacth.py** - файла настроек модуля вычисления разницы строк

* **logger_config.py** - файл для настроек логирования

* **parsing.py** - файл основного парсинга

* **updation.py** - файл настроек для запуска обновлений парсинга

* **validators.py** - файл функций для валидации данных

* **requirements.txt** -  Зависимости, необходимые для запуска бота


## Порядок развертывания, настройки и запуска проекта

**Перед началом работы необходимо создать и активировать виртуальное окружение!**

**Заполните .env файл по образцу**

**Запустите файлы asus_bot.py и updation.py**

```ini
python asus_bot.py
```

```ini
python updation.py
```

## Настройка и запуск проекта на удаленном серввере

**Создание systemd-юнитов**

1.
```ini
nano /etc/systemd/system/telegram_bot.service
```
```ini
[Unit]
Description=Telegram Bot Polling
After=network.target

[Service]
User=root
WorkingDirectory=/root/asus_bot/asus_bot
ExecStart=/root/asus_bot/venv/bin/python3 /root/asus_bot/asus_bot/asus_bot.py
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

2.
```ini
nano /etc/systemd/system/telegram_bot.service
```
```ini
[Unit]
Description=Telegram Bot Updating
After=network.target

[Service]
User=root
WorkingDirectory=/root/asus_bot/asus_bot
ExecStart=/root/asus_bot/venv/bin/python3 /root/asus_bot/asus_bot/updation.py
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

**Применение настроек и запуск сервисов**

```ini
systemctl daemon-reload
systemctl start telegram_bot
systemctl start telegram_bot_updation
systemctl enable telegram_bot
systemctl enable telegram_bot_updation
```

**Настройка сервиса Cron для автоматического перезапуска сервисов**

```ini
crontab -e
```
```ini
# добавьте строку в файл настроек (тут каждые 2 часа в 30 минут каждого часа)
30 */2 * * * systemctl restart telegram_bot.service ; systemctl restart telegram_bot_updation.service
```

## Автор проекта

[Виталий Мальков](https://github.com/ViolinistSpb)<br>
