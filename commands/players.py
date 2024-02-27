from commands import *
from util import is_correct_player_name
from sheet.player import signup as table_signup


@bot.message_handler(is_player=False, length=2, commands=['signup'])
@log_handler
def signup(message: telebot.types.Message):

    name = message.html_text.split()[1]

    if not is_correct_player_name(name):
        bot.send_message(message.chat.id, f"Имя {name} некорректно", parse_mode="html")
        return

    player = Player.get_or_none(Player.name == name)
    if player is not None:
        bot.send_message(message.chat.id, f"Имя {name} уже занято", parse_mode="html")
        return

    if not table_signup(name, message.from_user.id):
        bot.send_message(message.chat.id, f"Игрок с именем {name} не обнаружен в базе", parse_mode="html")
        return

    rights = Rights.PLAYER_DEFAULT
    player = Player.create(
        name=name,
        chat_id=message.from_user.id,
        rights=rights.value
    )

    bot.send_message(message.chat.id, f"Игрок {player.name} создан", parse_mode="html")


@bot.message_handler(is_player=True, commands=['signup'])
@log_handler
def signup(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Ты уже зарегистрирован в системе", parse_mode="html")


@bot.message_handler(is_player=False, commands=['signup'])
@log_handler
def signup(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Usage: /signup name", parse_mode="html")


@bot.message_handler(is_admin=True, length=3, commands=['change_player_name'])
@log_handler
def change_player_name(message: telebot.types.Message):
    player = Player.get_or_none(Player.name == message.html_text.split()[1])
    if player is None:
        bot.send_message(message.chat.id,
                         f"Нет пользователя с именем {message.html_text.split()[1]}",
                         parse_mode="html")
        return
    if not is_correct_player_name(message.html_text.split()[2]):
        bot.send_message(message.chat.id,
                         f"Некорректное имя {message.html_text.split()[2]}",
                         parse_mode="html")
        return
    player.name = message.html_text.split()[2]
    player.save()
    bot.send_message(message.chat.id,
                     f"Имя успешно заменено на {message.html_text.split()[2]}",
                     parse_mode="html")
    bot.send_message(player.chat_id,
                     f"Твое имя было изменено на {message.html_text.split()[2]}",
                     parse_mode="html")


@bot.message_handler(is_admin=True, length=3, commands=['change_player_move_duration'])
@log_handler
def change_player_move_duration(message: telebot.types.Message):
    player = Player.get_or_none(Player.name == message.html_text.split()[1])
    if player is None:
        bot.send_message(message.chat.id,
                         f"Нет пользователя с именем {message.html_text.split()[1]}",
                         parse_mode="html")
        return
    player.move_duration = int(message.html_text.split()[2])
    player.save()
    bot.send_message(message.chat.id,
                     f"Длительность движения заменена на {message.html_text.split()[2]}",
                     parse_mode="html")
    bot.send_message(player.chat_id,
                     f"Твою длительность перемещения изменили на {message.html_text.split()[2]} минут(у)",
                     parse_mode="html")


@bot.message_handler(is_super_admin=True, length=2, commands=['player_delete'])
@log_handler
def delete_player(message: telebot.types.Message):
    player = Player.get_or_none(Player.name == message.html_text.split()[1])
    if player is None:
        bot.send_message(message.chat.id,
                         f"Нет пользователя с именем {message.html_text.split()[1]}",
                         parse_mode="html")
        return
    player.delete_instance()
    bot.send_message(message.chat.id,
                     f"Пользователь удален",
                     parse_mode="html")
    bot.send_message(player.chat_id,
                     f"Тебя удалили из базы данных игры",
                     parse_mode="html")


@bot.message_handler(can_change_rights=True, length=3, commands=['player_add_right'])
@log_handler
def add_right(message: telebot.types.Message):
    player = Player.get_or_none(Player.name == message.html_text.split()[1])
    if player is None:
        bot.send_message(message.chat.id,
                         f"Нет пользователя с именем {message.html_text.split()[1]}",
                         parse_mode="html")
        return
    right = message.html_text.split()[2]
    if right not in Rights.__members__:
        bot.send_message(message.chat.id,
                         f"Нет такого права {right}",
                         parse_mode="html")
        return
    if player.add_right(Rights[right]):
        bot.send_message(message.chat.id,
                         f"Добавлено право {right}",
                         parse_mode="html")
        bot.send_message(player.chat_id,
                        f"Тебе выдали право {right}",
                        parse_mode="html")
    else:
        bot.send_message(message.chat.id,
                         f"Право не добавлено по внутренней причине",
                         parse_mode="html")


@bot.message_handler(can_change_rights=True, length=3, commands=['player_remove_right'])
@log_handler
def remove_right(message: telebot.types.Message):
    player = Player.get_or_none(Player.name == message.html_text.split()[1])
    if player is None:
        bot.send_message(message.chat.id,
                         f"Нет пользователя с именем {message.html_text.split()[1]}",
                         parse_mode="html")
        return
    right = message.html_text.split()[2]
    if right not in Rights.__members__:
        bot.send_message(message.chat.id,
                         f"Нет такого права {right}",
                         parse_mode="html")
        return
    if player.remove_right(Rights[right]):
        bot.send_message(message.chat.id,
                         f"Отнято право {right}",
                         parse_mode="html")
        bot.send_message(player.chat_id,
                        f"У тебя отнято право {right}",
                        parse_mode="html")
    else:
        bot.send_message(message.chat.id,
                         f"Право не отнято по внутренней причине",
                         parse_mode="html")
