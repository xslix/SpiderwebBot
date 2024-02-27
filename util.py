import re
import random

def is_correct_darknet_nick(nick):
    return re.match(r'^[a-zA-Z_0-9]{1,20}$', nick) is not None


def is_correct_player_name(name):
    return re.match(r'^[а-яА-Яa-zA-Z_0-9]{1,20}$', name) is not None


def is_correct_location_name(name):
    return is_correct_player_name(name)


def roll_dice(count, difficult=6, bonus=0):
    dices = []
    success_num = 0
    for _ in range(count):
        dice = random.randint(1, 10)
        if dice >= difficult:
            success_num += 1
            dices.append(f"<b>{dice}</b>")
        else:
            dices.append(str(dice))

    success_num += bonus
    return success_num, dices, difficult, bonus


def add_dices(success_num, dices, difficult, bonus, addition):
    for _ in range(addition):
        dice = random.randint(1, 10)
        if dice >= difficult:
            success_num += 1
            dices.append(f"<b>{dice}</b>")
        else:
            dices.append(str(dice))

    return success_num, dices, difficult, bonus


def get_roll_text(success_num, dices, difficult, bonus):
    text = f"Бросок: {', '.join(dices)}"
    if bonus > 0:
        text += f" + {bonus} автоуспех(-ов)"
    text += f".\nИтого: <b>{success_num}</b> успеха(-ов)."
    return text
