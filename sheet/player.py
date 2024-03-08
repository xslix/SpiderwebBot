from sheet import sheet
import datetime
import time
import pprint
import threading
from skills import *


data = []
update_time = datetime.datetime.now()
humanity_start_index = 3
skill_start_index = 9

writing_tread = threading.Thread()


def update_if_needed():
    if datetime.datetime.now() > update_time + datetime.timedelta(seconds=60):
        update()

def update():
   global data
   global update_time
   data = sheet.sheet.worksheet("Player").get('A3:AO', value_render_option='UNFORMATTED_VALUE')
   update_time = datetime.datetime.now()

update()


def broke_masquerade(user_id):
    update_if_needed()
    global writing_tread
    if writing_tread.is_alive():
        writing_tread.join()
    for i, row in enumerate(data):
        if len(row) > 10 and str(row[3]).lower() == str(user_id):
            row[10] += 1
            writing_tread = threading.Thread(target=lambda :sheet.sheet.worksheet("Player").update(range_name=f'K{3+i}', values=[[row[10]]], value_input_option='USER_ENTERED'))
            writing_tread.start()
            return


def signup(name, id):
    update_if_needed()
    for i, row in enumerate(data):
        if len(row) > 3 and str(row[0]).lower() == str(name).lower():
            row[3] = id
            global writing_tread
            if writing_tread.is_alive():
                writing_tread.join()

            writing_tread = threading.Thread(
                target=lambda: sheet.sheet.worksheet("Player").update(range_name=f'D{3 + i}', values=[[row[3]]],
                                                                      value_input_option='USER_ENTERED'))
            writing_tread.start()
            return True
    return False


def get_skill(user_id, name):
    update_if_needed()
    if name.lower() not in lower_skills:
        return False, 0
    index = lower_skills.index(name.lower())
    for row in data:
        if len(row) > 10 and str(row[3]).lower() == str(user_id):
            return True, row[11+index]
    return False, 0
