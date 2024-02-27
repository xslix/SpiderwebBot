from datetime import timedelta
import random

from telebot.types import ChatPermissions

from commands import *
from db import Rights


@bot.message_handler(is_admin=True, length=2, commands=['token_create'])
def add_token(message: telebot.types.Message):
    key = random.randrange(999999)
    exp = datetime.now() + timedelta(seconds=60 * 60 * 12)
    Token.create(
        key=key,
        type=message.html_text.split()[1],
        expiration=exp
    )
    bot.send_message(message.chat.id, f"Token {key} created until {exp.strftime('%H:%M:%S')}", parse_mode="html")


@bot.message_handler(is_admin=True, commands=['token_create'])
def add_token(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Usage: /token_create type", parse_mode="html")


@bot.message_handler(is_admin=True, length=1, commands=['clear_tokens'])
def add_token(message: telebot.types.Message):
    Token.delete()
    bot.send_message(message.chat.id, f"All tokens has been deleted", parse_mode="html")


@bot.message_handler(commands=['info'])
def info(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"User id: {message.from_user.id} Chat id: {message.chat.id}", parse_mode="html")


@bot.message_handler(is_admin=True, length=1, commands=['mute'])
def mute(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Переписка временно заблокирована МГ.", parse_mode="html")
    p = ChatPermissions(can_send_messages=False)
    bot.set_chat_permissions(message.chat.id, p)


@bot.message_handler(is_admin=True, length=1, commands=['unmute'])
def unmute(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Переписка вновь разрешена", parse_mode="html")
    p = ChatPermissions(can_send_messages=True)
    bot.set_chat_permissions(message.chat.id, p)


@bot.message_handler(is_admin=True, length=1, commands=['promote_admins'])
def add_location(message: telebot.types.Message):
    pp = Player.select()
    for p in filter(lambda x: x.has_right(Rights.ADMIN), pp):
        bot.promote_chat_member(message.chat.id,
                                p.chat_id,
                                True, True, True, True, True, True, True, True, False, True, True)


# @bot.message_handler(is_admin=True, length=1, commands=['set_darknet_admin_chat'])
# def set_darknet_admin_chat(message: telebot.types.Message):
#     Const.create(name=DARKNET_ADMIN_CHAT, value=message.chat.id)
#     bot.send_message(message.chat.id, f"Чат установлен как админский чат даркнета.", parse_mode="html")

@bot.message_handler(is_admin=True, length=1, commands=['set_issue_admin_chat'])
def set_issue_admin_chat(message: telebot.types.Message):
    Const.create(name=ISSUE_ADMIN_CHAT, value=message.chat.id)
    bot.send_message(message.chat.id, f"Чат установлен как админский чат заявок.", parse_mode="html")
