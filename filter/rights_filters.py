import telebot
from filter import *


class CanFight(telebot.custom_filters.SimpleCustomFilter):
    key = 'can_fight'
    @staticmethod
    def check(message: telebot.types.Message):
        p = Player.get_or_none(Player.chat_id == message.from_user.id)
        if p is None:
            return False
        return p.has_right(Rights.FIGHT)


bot.add_custom_filter(CanFight())


class IsSuperAdmin(telebot.custom_filters.SimpleCustomFilter):
    key = 'is_super_admin'
    @staticmethod
    def check(message: telebot.types.Message):
        p = Player.get_or_none(Player.chat_id == message.from_user.id)
        if p is None:
            return False
        return p.has_right(Rights.SUPER_ADMIN)


bot.add_custom_filter(IsSuperAdmin())


class IsPlayer(telebot.custom_filters.SimpleCustomFilter):
    key = 'is_player'
    @staticmethod
    def check(message: telebot.types.Message):
        p = Player.get_or_none(Player.chat_id == message.from_user.id)
        if p is None:
            return False
        return p.has_right(Rights.PLAYER)


bot.add_custom_filter(IsPlayer())

class IsAdmin(telebot.custom_filters.SimpleCustomFilter):
    key = 'is_admin'
    @staticmethod
    def check(message: telebot.types.Message):
        p = Player.get_or_none(Player.chat_id == message.from_user.id)
        if p is None:
            return False
        return p.has_right(Rights.ADMIN)


bot.add_custom_filter(IsAdmin())


class CanTeleport(telebot.custom_filters.SimpleCustomFilter):
    key = 'can_teleport'
    @staticmethod
    def check(message: telebot.types.Message):
        p = Player.get_or_none(Player.chat_id == message.from_user.id)
        if p is None:
            return False
        return p.has_right(Rights.TELEPORT)


bot.add_custom_filter(CanTeleport())


class CanMove(telebot.custom_filters.SimpleCustomFilter):
    key = 'can_move'
    @staticmethod
    def check(message: telebot.types.Message):
        p = Player.get_or_none(Player.chat_id == message.from_user.id)
        if p is None:
            return False
        return p.has_right(Rights.MOVE)


bot.add_custom_filter(CanMove())

class CanChangeRights(telebot.custom_filters.SimpleCustomFilter):
    key = 'can_change_rights'
    @staticmethod
    def check(message: telebot.types.Message):
        p = Player.get_or_none(Player.chat_id == message.from_user.id)
        if p is None:
            return False
        return p.has_right(Rights.CHANGE_RIGHTS)


bot.add_custom_filter(CanChangeRights())


class CanOverhear(telebot.custom_filters.SimpleCustomFilter):
    key = 'can_overhear'
    @staticmethod
    def check(message: telebot.types.Message):
        p = Player.get_or_none(Player.chat_id == message.from_user.id)
        if p is None:
            return False
        return p.has_right(Rights.OVERHEAR)


bot.add_custom_filter(CanOverhear())


class CanCall(telebot.custom_filters.SimpleCustomFilter):
    key = 'can_call'
    @staticmethod
    def check(message: telebot.types.Message):
        p = Player.get_or_none(Player.chat_id == message.from_user.id)
        if p is None:
            return False
        return p.has_right(Rights.CALL)


bot.add_custom_filter(CanCall())

