import datetime
import random
import threading
import time
from db.player import *
from db.location import *
from sheet.link import *
from bot import bot
from db import Token, Player
def start():
    x = threading.Thread(target=work)
    x.start()
    print(__name__ + " started")


def work():
    while True:
        locations = Location.select()
        for loc in locations:
            if datetime.datetime.now() < loc.next_gossip_time:
                continue
            players = Player.get_or_none(Player.current_location == loc.chat_id)
            if players is None:
                loc.next_gossip_time = datetime.datetime.now() + datetime.timedelta(minutes=random.randint(30, 60))
                loc.save()
                continue
            link = get_district_links(loc.name, 0, 1)
            if len(link) > 0:
                bot.send_message(loc.chat_id, f"<b>Прохожие обсуждают:</b> {link[0]}", parse_mode="html")
            loc.next_gossip_time = datetime.datetime.now() + datetime.timedelta(minutes=random.randint(30, 60))
            loc.save()
        time.sleep(1)
