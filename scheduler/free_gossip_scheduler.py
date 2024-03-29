import datetime
import random
import threading
import time
from db.player import *
from db.location import *
from sheet.link import *
from bot import bot
from db import Token, Player
from log import *
def start():
    x = threading.Thread(target=work)
    x.start()
    print(__name__ + " started")


def work():
    while True:
        try:
            locations = Location.select()
            for loc in locations:
                if datetime.datetime.now() < loc.next_gossip_time:
                    continue
                players = Player.get_or_none(Player.current_location == loc.chat_id)
                if players is None:
                    loc.next_gossip_time = datetime.datetime.now() + datetime.timedelta(minutes=random.randint(30, 60))
                    loc.save()
                    logging.info(f'В локации {loc.name} не найдено игроков для выдачи слухов')
                    continue
                link = get_district_links(loc.name, 0, 1)
                if len(link) > 0:
                    bot.send_message(loc.chat_id, f"<b>Прохожие обсуждают:</b> {link[0]}", parse_mode="html")
                    logging.info(f'В локации {loc.name} выдан слух {link[0]}')
                loc.next_gossip_time = datetime.datetime.now() + datetime.timedelta(minutes=random.randint(60, 90))
                loc.save()
            time.sleep(1)
        except Exception as e:
            print(f"TREAD EXCEPTION: {e}")
            print(__name__ + " restarted")