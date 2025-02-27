import os

from telegram import Bot, InputFile

from dotenv import load_dotenv

load_dotenv()

ASUS_BOT_TOKEN = os.getenv('ASUS_BOT_TOKEN', "")
chat_id = '1054725325'
file_path = 'event.ics'
bot = Bot(token=ASUS_BOT_TOKEN)


with open(file_path, 'rb') as file:
    bot.send_document(chat_id=chat_id, document=InputFile(file), caption="Вот ваш файл .ics!")
