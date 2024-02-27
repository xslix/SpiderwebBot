from bot import bot
from commands import *
from util import is_correct_location_name
from log import *


@bot.message_handler(is_admin=True, length=3, commands=['location_create'])
@log_handler
def add_location(message: telebot.types.Message):
    loc = Location.get_or_none(Location.name == message.html_text.split()[1])
    if loc is not None:
        bot.send_message(message.chat.id,
                         f"Локация с именем {loc.name} уже существует",
                         parse_mode="html")
        return

    loc = Location.get_or_none(Location.chat_id == message.chat.id)
    if loc is not None:
        bot.send_message(message.chat.id,
                         f"В данном чате уже существует локация {loc.name}",
                         parse_mode="html")
        return

    if not is_correct_location_name(message.html_text.split()[1]):
        bot.send_message(message.chat.id,
                         f"Некорректное имя локации {message.html_text.split()[1]}",
                         parse_mode="html")
        return
    stat = bot.get_chat_member(message.chat.id, bot.get_me().id).status
    if stat not in ['administrator', 'creator']:
        bot.send_message(message.chat.id,
                         "Бот не является администратором в данном чате",
                         parse_mode="html")
        return

    loc = Location.create(name=message.html_text.split()[1],
                          chat_id=message.chat.id,
                          is_private=message.html_text.split()[2] != 'True')
    bot.send_message(message.chat.id,
                     f"{'Приватная' if loc.is_private else 'Публичная'} локация {loc.name} создана",
                     parse_mode="html")


@bot.message_handler(is_admin=True, length=1, commands=['location_delete'])
@log_handler
def delete_location(message: telebot.types.Message):
    loc = Location.get_or_none(Location.chat_id == message.chat.id)
    if loc is None:
        bot.send_message(message.chat.id,
                         f"В данном чате нет локации",
                         parse_mode="html")
        return
    loc.delete_instance()
    bot.send_message(message.chat.id,
                     f"Локация {loc.name} удалена",
                     parse_mode="html")


@bot.message_handler(is_admin=True, commands=['location_list'])
@log_handler
def loclist(message: telebot.types.Message):
    loc = list(Location.select(Location.name).execute())
    bot.send_message(message.chat.id, ", ".join(map(lambda x: x.name, loc)), parse_mode="html")

