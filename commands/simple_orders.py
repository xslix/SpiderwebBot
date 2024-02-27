from datetime import timedelta
import random

from telebot.types import ChatPermissions

from commands import *
from db import Rights

from sheet import npc

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
