from datetime import timedelta
import random

from telebot.types import ChatPermissions

from commands import *
from db import Rights
from db import Player

from sheet import npc
from sheet.player import fix_masquerade

morph = ['Грубая сила', 'Восприятие', 'Обаяние', 'Социология', 'Ловкость рук', 'Ученость']

@bot.message_handler(is_player=True, commands=['mask', 'who', 'маска', 'кто'])
@log_handler
def mask(message: telebot.types.Message):
    name = message.text.split(' ', 1)[1].strip()
    bot.send_message(message.chat.id, npc.get_mask_by_name(name), parse_mode="html")


@bot.message_handler(is_player=True, commands=['gangrel', 'гангрел'])
@log_handler
def roll1d6(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Ты получаешь метаморфозу категории '{random.choice(morph)}'. Старая метаморфоза более не действительна.", parse_mode="html")

@bot.message_handler(is_player=True, commands=['mg', 'мг'])
@log_handler
def mg(message: telebot.types.Message):
    msg = ""
    for player in Player.select():
        if player.has_right(Rights.GAME_ADMIN):
            msg += f'<a href="tg://user?id={player.chat_id}">{player.name}</a> '
    bot.send_message(message.chat.id, msg, parse_mode="html")


@bot.message_handler(is_private=True, can_fix_masquerade=True,  commands=['fix'])
@log_handler
def fix(message: telebot.types.Message):
    fix_masquerade(message.from_user.id)
    bot.send_message(message.chat.id, 'Забвение применено.', parse_mode="html")
