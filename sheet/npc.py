from sheet import sheet
import datetime
import time
import pprint
import random

data = []
update_time = datetime.datetime.now()
evident = "Очевидный"
simple = "Обычный"

def update_if_needed():
    if datetime.datetime.now() > update_time + datetime.timedelta(seconds=60):
        update()

def update():
   global data
   global update_time
   data = sheet.sheet.worksheet("NPC").get('A2:S', value_render_option='FORMULA')
   update_time = datetime.datetime.now()

update()


def get_mask_by_name(name):
    update_if_needed()
    for row in data:
        if str(row[0]).lower() == name.lower():
            res = f"<b>{row[0]}</b> — {row[1]}.\n"
            if evident in row:
                res += f"Очевидные ходы:\n"
                if len(row) >= 8 and row[7] == evident:
                    res += f"{row[6]}\n"
                if len(row) >= 10 and row[9] == evident:
                    res += f"{row[8]}\n"
                if len(row) >= 12 and row[11] == evident:
                    res += f"{row[10]}\n"
            return res
    return "Нет совпадений."


def get_district_secrets(name, take):
    update_if_needed()
    secrets = []
    for row in data:
        if (len(row) > 5
                and str(row[3]).lower() == name.lower()
                and len(str(row[5])) > 0):
            secrets.append(f"{row[0]}: {row[5]}")
    random.shuffle(secrets)
    return secrets[:take]

def get_person_description(name, with_type):
    update_if_needed()
    for row in data:
        if str(row[0]).lower() == name.lower():
            res = f"<b>{row[0]}</b> — {row[1]}.\n"
            if with_type:
                res += row[2] + "\n"
            res += "Навыки: " + ", ".join([x for x in row[12:19] if x]) + "\n"
            if evident in row:
                res += f"Очевидные и обычные ходы:\n"
                if len(row) >= 8 and (row[7] == evident or row[7] == simple):
                    res += f"{row[6]}\n"
                if len(row) >= 10 and (row[9] == evident or row[9] == simple):
                    res += f"{row[8]}\n"
                if len(row) >= 12 and (row[11] == evident or row[11] == simple):
                    res += f"{row[10]}\n"
            return True, res
    return False, "Нет совпадений."