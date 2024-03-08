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
from sheet import link
from log import *

issues = {}

@bot.message_handler(is_player=True, commands=['личность', 'person'], is_private=True)
@log_handler
def person(message: telebot.types.Message):
    words = message.text.split(' ', 1)
    player = Player.get_or_none(Player.chat_id == message.from_user.id)
    if len(words) != 2:
        bot.send_message(message.chat.id, f"Использование команды: /личность [Имя персонажа]",
                         parse_mode="html")
        return
    name = words[1]
    with_type = player.has_right(Rights.SEE_PERSON_TYPE)
    success, desc = npc.get_person_description(name, with_type)
    if not success:
        bot.send_message(message.chat.id, f"Житель с таким именем не найден.", parse_mode="html")
        return

    bot.send_message(message.chat.id, f"Ты узнаешь:\n{desc}\n"
                                      f"Потрать 1 П.И. \n"
                                      f"Чтобы раскрыть его связи, используй /links [количество связей]",
                     parse_mode="html")
    issues[message.from_user.id] = (name, 0)

@bot.message_handler(is_player=True, length=2, commands=['связи', 'links'], is_private=True)
@log_handler
def links(message: telebot.types.Message):
    player = Player.get_or_none(Player.chat_id == message.from_user.id)
    count = 0
    if message.from_user.id not in issues:
        bot.send_message(message.chat.id, f"Чтобы раскрыть связи персонажа, сначала исследуй его с помощью /person",
                         parse_mode="html")
        return

    try:
        count = int(message.html_text.split()[1])
    except ValueError:
        bot.send_message(message.chat.id, f"Использование команды: /связи [число связей]",
                         parse_mode="html")
        return

    name, _ = issues[message.from_user.id]
    skill = random.choice(
        skills.skills_by_cats["Обаяние"] + skills.skills_by_cats["Восприятие"] + skills.skills_by_cats["Социология"])

    bot.send_message(message.chat.id, f"Ты ищешь {count} связей персонажа {name}.\n"
                                      f"Потрать {count} П.И. \n"
                                      f"Соверши бросок навыка <b>{skill}</b>, базовая сложность = 6.",
                     parse_mode="html")

    issues[message.from_user.id] = (name, count)
    player.roll_target = RollTarget.PERSON
    player.roll_status = RollStatus.WAITING_FOR_ROLL
    player.save()


@bot.message_handler(is_player=True, length=1, commands=['связи', 'links'], is_private=True)
@log_handler
def links(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Использование команды: /связи [число связей]",
                     parse_mode="html")
    return

def return_links(player_id, chat_id, suc_num):
    player = Player.get_or_none(Player.chat_id == player_id)
    if player_id not in issues.keys():
        player.roll_target = RollTarget.SIMPLE
        player.roll_status = RollStatus.NONE
        return
    (name, count) = issues[player_id]
    del issues[player_id]
    links = link.get_person_links(name, suc_num)
    if len(links) == 0:
        bot.send_message(chat_id, f"К сожалению, у этого персонажа нет связей с подходящей секретностью или просто их нет.", parse_mode="html")
        return
    bot.send_message(chat_id, f"Ты узнаешь: \n" + "\n".join(links), parse_mode="html")