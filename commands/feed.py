from datetime import timedelta
import random

from telebot.types import ChatPermissions
from bot import bot
from commands import *
from db import Rights
from db import Location
from db import Player
from db import RollTarget
from db import RollStatus
import skills
import random
from sheet import npc
from sheet.player import broke_masquerade
from log import *

issues = {}


@bot.message_handler(is_player=True, length=1, commands=['feed', 'корм'], is_private=True)
@log_handler
def feed(message: telebot.types.Message):

    player = Player.get_or_none(Player.chat_id == message.from_user.id)
    loc = Location.get_or_none(Location.chat_id == player.current_location)



    if message.from_user.id in issues.keys():
        bot.send_message(message.chat.id, f"Ты уже кормишься, используй /roll",
                         parse_mode="html")
        return

    skill = random.choice(skills.skills_by_cats["Грубая сила"])
    bot.send_message(message.chat.id, f"Ты агрессивно кормишься. Маскарад нарушен.\n"
                                      f"Потрать 1 П.И. \n"
                                      f"Соверши бросок навыка <b>{skill}</b>, базовая сложность = 6.",
                     parse_mode="html")
    issues[message.from_user.id] = 1
    broke_masquerade(message.from_user.id)
    player.roll_target = RollTarget.FEED
    player.roll_status = RollStatus.WAITING_FOR_ROLL
    player.save()


def return_feed(player_id, chat_id, suc_num):
    player = Player.get_or_none(Player.chat_id == player_id)
    if player_id not in issues.keys():
        player.roll_target = RollTarget.SIMPLE
        player.roll_status = RollStatus.NONE
        return
    name = issues[player_id]
    del issues[player_id]
    bot.send_message(chat_id, f"Восстанови {suc_num *2} П.К. Ты больше не можешь использовать этот ход до конца ночи.", parse_mode="html")