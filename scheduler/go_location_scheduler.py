import datetime
import threading
import time

from bot import bot
from db import Token, Player


def start():
    x = threading.Thread(target=work)
    x.start()
    print(__name__ + " started")


def work():
    while True:
        try:
            players = Player.select()
            for p in players:
                if datetime.datetime.now()-datetime.timedelta(seconds=1) < p.busy_until < datetime.datetime.now():
                    bot.send_message(p.chat_id, f"Время в пути вышло, можешь использовать /go чтобы войти в локацию")
            time.sleep(1)
        except Exception as e:
            print(f"TREAD EXCEPTION: {e}")
            print(__name__ + " restarted")
