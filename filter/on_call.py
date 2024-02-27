import telebot
from filter import *


class OnCall(telebot.custom_filters.SimpleCustomFilter):
    key = 'on_call'
    @staticmethod
    def check(message: telebot.types.Message):
        p = Call.get_or_none((Call.caller_id == message.from_user.id or Call.called_id == message.from_user.id) and Call.is_online)
        if p is None:
            return False
        return True


bot.add_custom_filter(OnCall())


class OnHorn(telebot.custom_filters.SimpleCustomFilter):
    key = 'on_horn'
    @staticmethod
    def check(message: telebot.types.Message):
        p = Call.get_or_none((Call.caller_id == message.from_user.id or Call.called_id == message.from_user.id) and not Call.is_online)
        if p is None:
            return False
        return True


bot.add_custom_filter(OnCall())
