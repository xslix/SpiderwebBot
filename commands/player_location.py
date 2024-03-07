from datetime import datetime
from datetime import timedelta
from  telebot.types import ReplyKeyboardRemove

from bot import bot
from commands import *
from db import Player
from commands.secrets import issues as secret_issues
from commands.gossips import issues as gossips_issues
from commands.person import issues as person_issues
from commands.feed import issues as feed_issues


@bot.message_handler(can_move=True, is_private=True, length=1, commands=['go', 'иду'])
@log_handler
def go(message: telebot.types.Message):
    player = Player.get_or_none(Player.chat_id == message.chat.id)
    if player.busy_until > datetime.now():
        bot.send_message(message.chat.id,
                         f"Ты еще в пути до <b>{player.busy_until.strftime('%H:%M:%S')}</b>",
                         parse_mode="html")
        return
    if player.current_location is not None:
        loc = Location.get_or_none(Location.chat_id == player.current_location)
        bot.send_message(message.chat.id,
                         f"Для начала выйди из локации <b>{loc.name}</b> с помощью команды <b>/exit</b>",
                         parse_mode="html")
        return
    loc = list(Location.select(Location.name).where(Location.is_private == False).execute())
    keyboard = types.InlineKeyboardMarkup()
    for l in loc:
        key = types.InlineKeyboardButton(text=l.name, callback_data=f"go {l.name}")
        keyboard.add(key)  # добавляем кнопку в клавиатуру
    bot.send_message(message.chat.id,
                     text="Выбери публичную локацию или введи \"/go адрес\" для перехода на скрытую",
                     reply_markup=keyboard)

# check button  callback
def is_go_call(call):
    words = call.data.split()
    if len(words) != 2:
        return False
    return words[0] == 'go'


@bot.callback_query_handler(func=is_go_call)
def callback_worker(call):
    name = call.data.split()[1]
    go_func(call.message, name)


@bot.message_handler(can_move=True, is_private=True, length=2, commands=['go', 'иду'])
@log_handler
def go_target(message: telebot.types.Message):
    name = message.html_text.split()[1]
    player = Player.get_or_none(Player.chat_id == message.chat.id)
    if player.busy_until > datetime.now():
        bot.send_message(message.chat.id,
                         f"Ты еще в пути до <b>{player.busy_until.strftime('%H:%M:%S')}</b>",
                         parse_mode="html")
        return
    if player.current_location is not None:
        loc = Location.get_or_none(Location.chat_id == player.current_location)
        bot.send_message(message.chat.id,
                         f"Для начала выйди из локации <b>{loc.name}</b> с помощью команды <b>/exit</b>",
                         parse_mode="html")
        return
    go_func(message, name)


def go_func(message, name):
    player = Player.get_or_none(Player.chat_id == message.chat.id)
    loc = Location.get_or_none(Location.name == name)
    if loc is None:
        bot.send_message(message.chat.id, f"Локации {name} не существует", parse_mode="html")
        return

    player.current_location = loc.chat_id
    player.coming_from = None
    player.save()
    bot.send_message(player.current_location,
                     f"Сюда кто-то направляется.",
                     parse_mode="html")
    bot.unban_chat_member(player.current_location, player.chat_id, True)
    link = bot.get_chat(loc.chat_id).invite_link
    bot.send_message(message.chat.id, f"<a href=\"{link}\">Вход в <b>{name}</b></a>", parse_mode="html")

@bot.message_handler(content_types=["new_chat_members"])
def foo(message):
    player = Player.get_or_none(Player.chat_id == message.from_user.id)
    if player is None:
        return
    if player.current_location == message.chat.id:
        bot.send_message(message.chat.id,
                         f"{player.name} заходит в локацию.",
                         parse_mode="html")
    else:
        bot.send_message(message.chat.id,
                         f"{player.name} заходит в локацию, но его не должно тут быть!.",
                         parse_mode="html")

@bot.message_handler(can_move=True, is_private=True, length=1, commands=['exit', 'выход'])
@log_handler
def exit(message: telebot.types.Message):
    player = Player.get_or_none(Player.chat_id == message.chat.id)
    if player.current_location is None:
        bot.send_message(message.chat.id, f"Ты не находишься в локации", parse_mode="html")
        return

    player.coming_from = player.current_location
    player.busy_until = datetime.now() + timedelta(minutes=player.move_duration)
    bot.send_message(player.current_location,
                     f"{player.name} уходит.",
                     parse_mode="html")
    for loc in Location.select():
        try:
            bot.ban_chat_member(loc.chat_id,
                                player.chat_id,
                                int((datetime.now() + timedelta(minutes=1)).timestamp()))
        except Exception as e:
            pass
    player.current_location = None
    player.save()
    bot.send_message(message.chat.id,
                     f"Локация покинута, ты будешь в пути до <b>{player.busy_until.strftime('%H:%M:%S')}</b>",
                     parse_mode="html")

    if message.from_user.id in secret_issues.keys():
        del(secret_issues[message.from_user.id])
    if message.from_user.id in person_issues.keys():
        del(person_issues[message.from_user.id])
    if message.from_user.id in gossips_issues.keys():
        del(gossips_issues[message.from_user.id])
    if message.from_user.id in feed_issues.keys():
        del(feed_issues[message.from_user.id])



@bot.message_handler(can_teleport=True, is_private=True, length=2, commands=['tp', 'тп'])
@log_handler
def teleport_target(message: telebot.types.Message):
    name = message.html_text.split()[1]
    player = Player.get_or_none(Player.chat_id == message.chat.id)
    if player.current_location is not None:
        bot.ban_chat_member(player.current_location,
                            player.chat_id,
                            int((datetime.now() + timedelta(minutes=1)).timestamp()))
        bot.send_message(player.current_location,
                         f"{player.name} исчезает бесследно.",
                         parse_mode="html")

    player.busy_until = datetime.now()
    player.save()

    loc = Location.get_or_none(Location.name == name)
    if loc is None:
        bot.send_message(message.chat.id, f"Локации {name} не существует", parse_mode="html")
        return

    if player.coming_from is not None:
        from_loc = Location.get_or_none(Location.chat_id == player.coming_from)
        if from_loc is not None and from_loc.chat_id == loc.chat_id:
            bot.send_message(message.chat.id,
                             f"Нельзя вернуться в локацию, из которой начался путь",
                             parse_mode="html")
            return
    player.current_location = loc.chat_id
    player.coming_from = None
    player.save()
    bot.unban_chat_member(player.current_location, player.chat_id, True)
    link = bot.get_chat(loc.chat_id).invite_link
    bot.send_message(message.chat.id, f"<a href=\"{link}\">Вход в <b>{name}</b></a>", parse_mode="html")

