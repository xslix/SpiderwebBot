import random
import telebot
from bot import bot
from datetime import datetime, timedelta
from commands import *
import log

while True:
    try:
        print("Start polling")
        bot.polling(non_stop=True, interval=0)
    except  Exception as e:
        logging.exception("MAIN EXCEPTION:")
