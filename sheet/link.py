from sheet import sheet
import datetime
import time
import pprint
import random

data = []
update_time = datetime.datetime.now()
evident = "Очевидный"


def update_if_needed():
    if datetime.datetime.now() > update_time + datetime.timedelta(seconds=60):
        update()


def update():
    global data
    global update_time
    data = sheet.sheet.worksheet("Link").get('A2:F', value_render_option='UNFORMATTED_VALUE')
    update_time = datetime.datetime.now()


update()


def get_mask_by_name(name):
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


def get_char_links(name, secret=99, take=999):
    links = []
    for row in data:
        if (str(row[0]).lower() == name.lower()
                or str(row[1]).lower() == name.lower())\
                and len(row) > 2\
                and secret >= int(row[2]):
            links.append(str(row[3]))
    random.shuffle(links)
    return links[:take]


def get_district_links(name, secret=99, take=999):
    links = []
    for row in data:
        if (len(row) > 5
                and (str(row[4]).lower() == name.lower()
                     or str(row[5]).lower() == name.lower())
                and row[2] != "" and row[3] != "" and secret >= int(row[2])):
            links.append(str(row[3]))
    random.shuffle(links)
    return links[:take]


def get_person_links(name, secret=99, take=999):
    links = []
    for row in data:
        if (len(row) > 5
                and (str(row[0]).lower() == name.lower()
                     or str(row[1]).lower() == name.lower())
                and secret >= int(row[2])):
            links.append(str(row[3]))
    random.shuffle(links)
    return links[:take]
