from datetime import datetime
from datetime import timedelta

from bot import bot
from commands import *
from db import Player
from log import *



@bot.message_handler(is_player=True, length=2, is_private=True, on_call=False, on_horn=False, commands=['call', 'звонок'])
@log_handler
def call(message: telebot.types.Message):
    name = message.text.split()[1]
    player = Player.get_or_none(Player.chat_id == message.chat.id)
    called = Player.get_or_none(Player.name == name)

    if called is None:
        bot.send_message(message.chat.id,
                         f"Персонаж '{name}' не найден",
                         parse_mode="html")
        return
    call = Call.get_or_none((Call.called_id == called.chat_id) | (Call.caller_id == called.chat_id))
    if call is not None:
        bot.send_message(message.chat.id, f"Номер занят. Короткие гудки.", parse_mode="html")
        return

    call = Call.create(caller_id=message.from_user.id,
                       called_id=called.chat_id,
                       is_online=False,
                       end_timestamp=datetime.now()+timedelta(minutes=5))
    call.save()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Положить трубку", callback_data=f"call drop"))
    bot.send_message(message.chat.id,
                     f"Набираем номер '{name}', ждем ответа. Гудки...",
                     parse_mode="html", reply_markup=keyboard)

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Принять", callback_data=f"call answer"))
    keyboard.add(types.InlineKeyboardButton(text="Сбросить", callback_data=f"call drop"))

    bot.send_message(called.chat_id,
                     f"Входящий звонок от'{player.name}', будешь ли брать трубку? (Это бесплатно)",
                     parse_mode="html", reply_markup=keyboard)



@bot.message_handler(is_player=True, length=1, is_private=True, commands = ['drop', 'сбросить'])
@log_handler
def drop_call(message: telebot.types.Message, forced_id=0):
    if forced_id != 0:
        message.from_user.id = forced_id
    call = Call.get_or_none((Call.called_id == message.from_user.id) | (Call.caller_id == message.from_user.id))
    if call is None:
        bot.send_message( message.from_user.id,
                         f"Завершаемый звонок не найден",
                         parse_mode="html")
        return

    bot.send_message( message.from_user.id,
                     f"Звонок окончен/отменен.",
                     parse_mode="html")

    bot.send_message(call.called_id if int(message.from_user.id) == int(call.caller_id) else call.caller_id,
                     f"Абонент завершил вызов.",
                     parse_mode="html")
    call.delete_instance()


@bot.message_handler(is_player=True, length=1, is_private=True, commands=['answer', 'принять'])
@log_handler
def answer_call(message: telebot.types.Message, forced_id=0):
    if forced_id != 0:
        message.from_user.id = forced_id
    call = Call.get_or_none((Call.called_id == message.from_user.id) & (Call.is_online == False))
    if call is None:
        bot.send_message(message.from_user.id,
                         f"Входящий звонок не найден",
                         parse_mode="html")
        return
    call.is_online = True
    call.end_timestamp = datetime.now()+timedelta(minutes=30)
    call.save()
    bot.send_message(call.caller_id,
                     f"Абонент поднял трубку. Звонок активен. Потрать 50$. Используй /drop /сбросить, чтобы завершить звонок.",
                     parse_mode="html")
    bot.send_message(call.called_id,
                     f"Звонок активен. Используй /drop /сбросить, чтобы завершить звонок.",
                     parse_mode="html")



@bot.message_handler(is_player=True, length=1, is_private=True, commands=['call', 'звонок'])
@log_handler
def call(message: telebot.types.Message):
    bot.send_message(message.chat.id,
                     f"Использование команды: /звонок [имя персонажа]",
                     parse_mode="html")


def is_call_call(call):
    words = call.data.split()
    if len(words) != 2:
        return False
    return words[0] == 'call'


@bot.callback_query_handler(func=is_call_call)
def callback_worker(call):
    if call.data.split()[1] == "drop":
        drop_call(call.message, call.from_user.id)
    if call.data.split()[1] == "answer":
        answer_call(call.message, call.from_user.id)


@bot.message_handler(is_player=True, is_private=True, on_call=True)
@log_handler
def talk(message: telebot.types.Message):
    player = Player.get_or_none(Player.chat_id == message.from_user.id)
    call = Call.get_or_none((Call.caller_id == message.from_user.id) & (Call.is_online))
    if call is None:
        call = Call.get_or_none((Call.called_id == message.from_user.id )& (Call.is_online))
    if call is None:
        return
    chat_id = call.caller_id if int(call.called_id) == int(message.from_user.id) else call.called_id
    bot.send_message(chat_id,
                     f"<b>{player.name}:</b> {message.text}",
                     parse_mode="html")

