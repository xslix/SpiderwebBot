import peewee as pw
from datetime import datetime
from db import DbModel


class Token(DbModel):
    id = pw.AutoField(column_name='id')
    key = pw.IntegerField(column_name='key', null=False)
    type = pw.TextField(column_name='type', null=False)
    expiration = pw.TimestampField(column_name="expiration", null=False)

    class Meta:
        table_name = 'Token'

    def is_valid(self, type):
        return datetime.now() < self.expiration and type == self.type


Token.create_table()