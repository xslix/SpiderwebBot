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


issues = {}


@bot.message_handler(is_player=True, length=1, commands=['секреты', 'secrets'], is_private=True)
@log_handler
def secrets(message: telebot.types.Message):

    player = Player.get_or_none(Player.chat_id == message.from_user.id)
    loc = Location.get_or_none(Location.chat_id == player.current_location)

    if loc is None or player.current_location != int(loc.chat_id):
        bot.send_message(message.chat.id, f"Ты должен находиться в локации района, чтобы копать секреты.",
                         parse_mode="html")
        return

    name = loc.name

    if message.from_user.id in issues.keys():
        bot.send_message(message.chat.id, f"Ты уже копаешь секреты в {name}, используй /roll",
                         parse_mode="html")
        return

    skill = random.choice(
        skills.skills_by_cats["Ловкость рук"] + skills.skills_by_cats["Восприятие"] + skills.skills_by_cats["Ученость"])
    bot.send_message(message.chat.id, f"Ты копаешь секреты в районе {loc.name}.\n"
                                      f"Потрать 3 П.И. \n"
                                      f"Соверши бросок навыка <b>{skill}</b>, базовая сложность = 6.",
                     parse_mode="html")
    issues[message.from_user.id] = name
    player.roll_target = RollTarget.SECRET
    player.roll_status = RollStatus.WAITING_FOR_ROLL
    player.save()


def return_secrets(player_id, chat_id, suc_num):
    player = Player.get_or_none(Player.chat_id == player_id)
    if player_id not in issues.keys():
        player.roll_target = RollTarget.SIMPLE
        player.roll_status = RollStatus.NONE
        return
    name = issues[player_id]
    del issues[player_id]
    secrets = npc.get_district_secrets(name, suc_num)
    bot.send_message(chat_id, f"Ты узнаешь: \n" + "\n".join(secrets), parse_mode="html")