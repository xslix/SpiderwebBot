import peewee as pw
from db import DbModel, Rights
from datetime import datetime


class Spy(DbModel):
    id = pw.AutoField(column_name='id')
    chat_id = pw.IntegerField(column_name='chat_id', null=True)
    overhear_location = pw.IntegerField(column_name='overhear_location', null=True)
    overhear_until = pw.TimestampField(column_name="overhear_until")


    class Meta:
        table_name = 'Spy'


Spy.create_table()