import datetime
import threading
import time

from db import Token


def start():
    x = threading.Thread(target=work)
    x.start()
    print(__name__ + " started")


def work():
    while True:
        Token.delete().where(Token.expiration < datetime.datetime.now()).execute()
        time.sleep(10)