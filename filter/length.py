import telebot
from filter import *


class Length(telebot.custom_filters.SimpleCustomFilter):
    key = 'length'
    @staticmethod
    def check(message: telebot.types.Message):
        return len(message.html_text.split())


bot.add_custom_filter(Length())
