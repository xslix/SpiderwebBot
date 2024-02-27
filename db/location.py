from db import *
import peewee as pw
from datetime import datetime


class Location(DbModel):
    id = pw.AutoField(column_name='Id')
    name = pw.TextField(column_name='Name', null=True)
    chat_id = pw.TextField(column_name='ChatId', null=False)
    is_private = pw.BooleanField(column_name='IsPrivate', null=False)
    next_gossip_time = pw.TimestampField(column_name="busy_until", null=datetime.now())

    class Meta:
        table_name = 'Location'


Location.create_table()

