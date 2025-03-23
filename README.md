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

## Автор проекта

[Виталий Мальков](https://github.com/ViolinistSpb)<br>
