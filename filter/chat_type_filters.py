import telebot
from filter import *


class IsPrivate(telebot.custom_filters.SimpleCustomFilter):
    key = 'is_private'
    @staticmethod
    def check(message: telebot.types.Message):
        return message.chat.id == message.from_user.id


bot.add_custom_filter(IsPrivate())


class IsLocation(telebot.custom_filters.SimpleCustomFilter):
    key = 'is_location'
    @staticmethod
    def check(message: telebot.types.Message):
        loc = Location.get_or_none(Location.chat_id == message.chat.id)
        return loc is not None


bot.add_custom_filter(IsLocation())

