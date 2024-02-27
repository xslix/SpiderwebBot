from datetime import timedelta
import random

from telebot.types import ChatPermissions

from commands import *
from db import Rights
from db import Player
from db import RollStatus
from db import RollTarget
import util
import commands.gossips
import commands.secrets
from sheet.player import broke_masquerade
from sheet.player import get_skill
from log import *

current_rolls = {}

@bot.message_handler(is_player=True, commands=['roll', 'ролл'])
@log_handler
def roll(message: telebot.types.Message):
    words = message.html_text.split()
    if len(words) == 2:
        words.append(6)
        words.append(0)
    elif len(words) == 3:
        words.append(0)
    elif len(words) != 4:
        bot.send_message(message.chat.id, f"Использование: /roll [Количество кубов или навык] [Сложность = 6] [Автоуспехов = 0]",
                         parse_mode="html")
        return
    try:
        count = int(words[1])
    except ValueError:
        (suc, skill) = get_skill(message.from_user.id, words[1])
        if not suc:
            bot.send_message(message.chat.id,
                             f"Заданный навык не найден",
                             parse_mode="html")
            return
        count = skill
    try:
        difficult = int(words[2])
        bonus = int(words[3])
    except ValueError:
        bot.send_message(message.chat.id, f"Использование: /roll [Количество кубов или навык] [Сложность = 6] [Автоуспехов = 0]",
                         parse_mode="html")
        return
    if count > 15 or bonus > 15 or difficult > 10 or difficult < 1:
        bot.send_message(message.chat.id,
                         f"Подозреваем, ты опечатался в аргументах. Сделай бросок повторно.",
                         parse_mode="html")
        return

    player = Player.get_or_none(Player.chat_id == message.from_user.id)
    success_num, dices, difficult, bonus = util.roll_dice(count, difficult, bonus)

    roll_text = util.get_roll_text(success_num, dices, difficult, bonus)
    current_rolls[message.from_user.id] = (message.chat.id, success_num, dices, difficult, bonus)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Нарушить Маскарад", callback_data=f"reroll маскарад"))
    keyboard.add(types.InlineKeyboardButton(text="Обратиться к зверю", callback_data=f"reroll зверь"))
    keyboard.add(types.InlineKeyboardButton(text="Принять результат", callback_data=f"reroll нет"))
    bot.send_message(message.chat.id, f"{roll_text}\nБудешь ли улучшать бросок? (/masq /beast /no)",
                     parse_mode="html", reply_markup=keyboard)
    player.roll_status = RollStatus.WAITING_FOR_ANY_REROLL
    player.save()


@bot.message_handler(is_player=True, length=1, commands=['masq', 'маскарад'])
@log_handler
def masquerade(message: telebot.types.Message, forced_id=0):
    if forced_id != 0:
        message.from_user.id = forced_id
    player = Player.get_or_none(Player.chat_id == message.from_user.id)
    chat_id, success_num, dices, difficult, bonus = 0, 0, 0, 0, 0
    if message.from_user.id not in current_rolls.keys():
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Да", callback_data=f"reroll brake"))
        bot.send_message(message.chat.id, f"Улучшаемый бросок не найден. Нарушить маскарад по другим причинам?",
                         parse_mode="html", reply_markup=keyboard)
        return
    elif player.roll_status != RollStatus.WAITING_FOR_ANY_REROLL and player.roll_status != RollStatus.WAITING_FOR_MASQUERADE:
        bot.send_message(message.chat.id, f"Этот бросок нельзя улучшить, нарушив маскарад.", parse_mode="html")
    else:
        chat_id, success_num, dices, difficult, bonus = current_rolls[message.from_user.id]
        success_num, dices, difficult, bonus = util.roll_dice(len(dices), difficult, bonus)
        broke_masquerade(message.from_user.id)

    if player.roll_status == RollStatus.WAITING_FOR_ANY_REROLL:
        player.roll_status = RollStatus.WAITING_FOR_BEAST
        player.save()
        current_rolls[message.from_user.id] = (message.chat.id, success_num, dices, difficult, bonus)
        roll_text = util.get_roll_text(success_num, dices, difficult, bonus)
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Обратиться к зверю", callback_data=f"reroll зверь"))
        keyboard.add(types.InlineKeyboardButton(text="Принять результат", callback_data=f"reroll нет"))
        bot.send_message(message.chat.id, f"{roll_text}\nБудешь ли улучшать бросок? (/beast /end)",
                         parse_mode="html", reply_markup=keyboard)
        return
    else:
        player.roll_status = RollStatus.ENDED
        player.save()
        current_rolls[message.from_user.id] = (message.chat.id, success_num, dices, difficult, bonus)
        end_roll(message.from_user.id)


@bot.message_handler(is_player=True, length=1, commands=['beast', 'зверь'])
@log_handler
def beast(message: telebot.types.Message, forced_id=0):
    if forced_id != 0:
        message.from_user.id = forced_id
    player = Player.get_or_none(Player.chat_id == message.from_user.id)
    chat_id, success_num, dices, difficult, bonus = 0, 0, 0, 0, 0
    if message.from_user.id not in current_rolls.keys():
        bot.send_message(message.chat.id, f"Улучшаемый бросок не найден.", parse_mode="html")
        return
    elif player.roll_status != RollStatus.WAITING_FOR_ANY_REROLL and player.roll_status != RollStatus.WAITING_FOR_BEAST:
        bot.send_message(message.chat.id, f"Этот бросок нельзя улучшить, поддавшись зверю.", parse_mode="html")
    else:
        chat_id, success_num, dices, difficult, bonus = current_rolls[message.from_user.id]
        add = 6 if player.has_right(Rights.IMPROVED_BEAST) else 4
        success_num, dices, difficult, bonus = util.add_dices(success_num, dices, difficult, bonus, add)

    if player.roll_status == RollStatus.WAITING_FOR_ANY_REROLL:
        player.roll_status = RollStatus.WAITING_FOR_MASQUERADE
        player.save()
        current_rolls[message.from_user.id] = (message.chat.id, success_num, dices, difficult, bonus)
        roll_text = util.get_roll_text(success_num, dices, difficult, bonus)
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Нарушить Маскарад", callback_data=f"reroll маскарад"))
        keyboard.add(types.InlineKeyboardButton(text="Принять результат", callback_data=f"reroll нет"))
        bot.send_message(message.chat.id, f"<b>Потеряй человеческую добродетель. Если у тебя осталось меньше 3, обратись к МГ.</b>\n{roll_text}\nБудешь ли улучшать бросок? (/masq /end)",
                         parse_mode="html", reply_markup=keyboard)
        return
    else:
        player.roll_status = RollStatus.ENDED
        player.save()
        current_rolls[message.from_user.id] = (message.chat.id, success_num, dices, difficult, bonus)
        end_roll(message.from_user.id)


@bot.message_handler(is_player=True, length=1, commands=['end', 'нет'])
@log_handler
def no_roll(message: telebot.types.Message, forced_id=0):
    if forced_id != 0:
        message.from_user.id = forced_id
    if message.from_user.id not in current_rolls.keys():
        bot.send_message(message.chat.id, f"Активный бросок не найден.", parse_mode="html")
    else:
        end_roll(message.from_user.id)


def end_roll(user_id):
    player = Player.get_or_none(Player.chat_id == user_id)
    player.roll_status = RollStatus.NONE
    player.save()
    chat_id, success_num, dices, difficult, bonus = current_rolls[user_id]
    del current_rolls[user_id]
    roll_text = util.get_roll_text(success_num, dices, difficult, bonus)
    bot.send_message(chat_id, f"{roll_text}", parse_mode="html")
    if player.roll_target == RollTarget.GOSSIP:
        return_gossips(user_id, chat_id, success_num)
    elif player.roll_target == RollTarget.SECRET:
        return_secrets(user_id, chat_id, success_num)
    elif player.roll_target == RollTarget.PERSON:
        return_links(user_id, chat_id, success_num)
    elif player.roll_target == RollTarget.FEED:
        return_feed(user_id, chat_id, success_num)


def is_reroll_call(call):
    words = call.data.split()
    if len(words) != 2:
        return False
    return words[0] == 'reroll'

def hard_brake(chat_id, user_id):
    broke_masquerade(user_id)
    bot.send_message(message.chat.id,f"Маскарад нарушен.", parse_mode="html")



@bot.callback_query_handler(func=is_reroll_call)
def callback_worker(call):
    if call.data.split()[1] == "маскарад":
        masquerade(call.message, call.from_user.id)
    if call.data.split()[1] == "зверь":
        beast(call.message, call.from_user.id)
    if call.data.split()[1] == "нет":
        no_roll(call.message, call.from_user.id)
    if call.data.split()[1] == "brake":
        hard_brake(call.message.chat.id, call.from_user.id)


