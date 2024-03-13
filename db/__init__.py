from enum import IntEnum, Enum, unique

import peewee as pw
import json

conn = pw.SqliteDatabase("db.db")
conn.close()

DARKNET_ADMIN_CHAT = "darknet_admin_chat"
ISSUE_ADMIN_CHAT = "issue_admin_chat"


@unique
class Rights(Enum):
    BOT_ADMIN = 2**0
    GAME_ADMIN = 2**1
    PLAYER = 2**2
    LOCK_LOCATION = 2**3
    MOVE = 2**4
    TELEPORT = 2**5
    FIGHT = 2**6
    OVERHEAR = 2**7
    CHANGE_RIGHTS = 2**8
    CALL = 2 ** 9
    IMPROVED_BEAST = 2 ** 10
    SEE_PERSON_TYPE = 2 ** 11
    FIX_MASQUERADE = 2 ** 12

    ADMIN = PLAYER | GAME_ADMIN | LOCK_LOCATION | FIGHT | CALL | MOVE
    SUPER_ADMIN = ADMIN | BOT_ADMIN | CHANGE_RIGHTS
    PLAYER_DEFAULT = PLAYER | MOVE | FIGHT | CALL
    ALL = (2**20)-1

@unique
class RollTarget(IntEnum):
    SIMPLE = 0
    DAMAGE = 1
    GOSSIP = 2
    SECRET = 3
    PERSON = 4
    FEED = 5


@unique
class RollStatus(IntEnum):
    NONE = 0
    WAITING_FOR_ROLL = 1
    WAITING_FOR_ANY_REROLL = 2
    WAITING_FOR_MASQUERADE = 3
    WAITING_FOR_BEAST = 4
    ENDED = 5


class DbModel(pw.Model):
    class Meta:
        database = conn


from db.location import *
from db.player import *
from db.token import *
from db.call import *
from db.var import *