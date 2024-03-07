from db import *
import peewee as pw


class Call(DbModel):
    id = pw.AutoField(column_name='id')
    caller_id = pw.TextField(column_name='caller_id', null=True)
    called_id = pw.TextField(column_name='called_id', null=False)
    end_timestamp = pw.TimestampField(column_name="end_timestamp", null=datetime.now())
    is_online = pw.BooleanField(column_name='is_inline', null=False)
    class Meta:
        table_name = 'Call'


Call.drop_table()
Call.create_table()
