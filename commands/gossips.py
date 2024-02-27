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
from sheet import link

issues = {}


@bot.message_handler(is_player=True, length=2, commands=['слухи', 'rumors'], is_private=True)
@log_handler
def gossips(message: telebot.types.Message):
    try:
        count = int(message.html_text.split()[1])
    except ValueError:
        bot.send_message(message.chat.id, f"Использование команды: /слухи [число слухов]",
                         parse_mode="html")
        return
    player = Player.get_or_none(Player.chat_id == message.from_user.id)
    loc = Location.get_or_none(Location.chat_id == player.current_location)

    if loc is None or player.current_location != int(loc.chat_id):
        bot.send_message(message.chat.id, f"Ты должен находиться в локации района, чтобы искать слухи.", parse_mode="html")
        return

    name = loc.name

    if message.from_user.id in issues.keys():
        bot.send_message(message.chat.id, f"Ты уже ищешь слухи в {name}, используй /roll",
                         parse_mode="html")
        return

    skill = random.choice(skills.skills_by_cats["Обаяние"] + skills.skills_by_cats["Восприятие"] + skills.skills_by_cats["Ученость"])
    bot.send_message(message.chat.id, f"Ты ищешь {count} слух(-ов) в районе {loc.name}.\n"
                                      f"Потрать {count} П.И. \n"
                                      f"Соверши бросок навыка <b>{skill}</b>, базовая сложность = 6.", parse_mode="html")
    issues[message.from_user.id] = (name, count)
    player.roll_target = RollTarget.GOSSIP
    player.roll_status = RollStatus.WAITING_FOR_ROLL
    player.save()


def return_gossips(player_id, chat_id, suc_num):
    player = Player.get_or_none(Player.chat_id == player_id)
    if player_id not in issues.keys():
        player.roll_target = RollTarget.SIMPLE
        player.roll_status = RollStatus.NONE
        return
    name, count = issues[player_id]
    del issues[player_id]
    links = link.get_district_links(name, suc_num, count)
    bot.send_message(chat_id, f"Ты узнаешь: \n" + "\n".join(links), parse_mode="html")


@bot.message_handler(is_player=True, length=1, commands=['слухи', 'rumors'])
@log_handler
def gossips(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Использование команды: /слухи [число слухов]", parse_mode="html")
