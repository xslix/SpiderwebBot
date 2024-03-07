import random
import telebot
from bot import bot
from datetime import datetime, timedelta
from commands import *
import log
from telebot.util import update_types
import time
from scheduler import *

while True:
    try:
        print("Start polling")

        bot.polling(non_stop=True, interval=0, allowed_updates=update_types)
        time.sleep(1)
    except Exception as e:
        logging.exception("MAIN EXCEPTION:")
        print(f"MAIN EXCEPTION: {e}")
