from dotenv import load_dotenv
import os

from telegram import Bot
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater, Filters, MessageHandler


load_dotenv()

ASUS_BOT_TOKEN = os.getenv('ASUS_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

bot = Bot(token=ASUS_BOT_TOKEN)
updater = Updater(token=ASUS_BOT_TOKEN)
text = 'Для начала работы введите /start'

bot.send_message(TELEGRAM_CHAT_ID, text)


def say_hi(update, context):
    chat = update.effective_chat
    if update.message.text == 'Войти в систему asus':
        context.bot.send_message(chat_id=chat.id, text='Чуть позже!')
    else:
        context.bot.send_message(chat_id=chat.id, text='Hi!')
    print(update)
    print(update.message.chat.id)


def wake_up(update, context):
    chat = update.effective_chat
    user = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['/start', 'Войти в систему asus']])
    context.bot.send_message(
        chat_id=chat.id,
        text=f'{user}, спасибо что присодинился к асус-боту!',
        reply_markup=button
    )


updater.dispatcher.add_handler(CommandHandler('start', wake_up))
updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))

updater.start_polling()
updater.idle()
