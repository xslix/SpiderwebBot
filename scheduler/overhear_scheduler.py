import datetime
import threading
import time

from db import Spy


def start():
    x = threading.Thread(target=work)
    x.start()
    print(__name__ + " started")


def work():
    while True:
        Spy.delete().where(Spy.overhear_until < datetime.datetime.now()).execute()
        time.sleep(1)