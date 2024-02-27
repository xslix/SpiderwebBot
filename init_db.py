from db import *

Location.drop_table()
Player.drop_table()
Token.drop_table()
Call.drop_table()

Location.create_table()
Player.create_table()
Token.create_table()
Call.create_table()


Player.create(chat_id=215504513, name='Elisan', rights=Rights.SUPER_ADMIN.value)