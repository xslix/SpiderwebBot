import logging
import telebot
from db import Player


logging.basicConfig(filename='handle.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
telebot.logger.setLevel(logging.INFO)
telebot.logger.addHandler(logging.FileHandler('telebot.log'))

def log_handler(func):
    def wrapper(message: telebot.types.Message, *args, **kwargs):
        player = Player.get_or_none(Player.chat_id == message.from_user.id)
        if player is None:
            logging.info(f'Вызов функции {func.__name__} user_id: {message.from_user.id} - chat_id: {message.chat.id} - text: {message.text}')
        else:
            logging.info(
                f'Вызов функции {func.__name__} user_id: {message.from_user.id} ({player.name}) - chat_id: {message.chat.id} - text: {message.text}')
        result = func(message, *args, **kwargs)
        logging.info(f'Функция {func.__name__} завершена')
        return result
    return wrapper