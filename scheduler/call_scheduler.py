import random
import threading
import time

from db.player import *
from db.call import *
from sheet.link import *

from bot import bot
from db import Token, Player

def start():
    x = threading.Thread(target=work)
    x.start()
    print(__name__ + " started")


def work():
    while True:
        try:
            calls = Call.select()
            for call in calls:
                if call.end_timestamp < datetime.datetime.now():
                    bot.send_message(call.called_id, f"Звонок завершен по времени.", parse_mode="html")
                    bot.send_message(call.caller_id, f"Звонок завершен по времени.", parse_mode="html")
                    call.delete_instance()
            time.sleep(1)
        except Exception as e:
            print(f"TREAD EXCEPTION: {e}")
            print(__name__ + " restarted")
