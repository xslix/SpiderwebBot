from pprint import pprint

import gspread

gc = gspread.service_account()

sheet = gc.open_by_key("1qfQFqDLCqcTllIjfEdA6E-Tz5sgaiO1MrZLytR9z9s8")