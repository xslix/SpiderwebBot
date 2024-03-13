from db import *
import peewee as pw
from datetime import datetime
from db import DbModel


class Var(DbModel):
    id = pw.AutoField(column_name='Id')
    name = pw.TextField(column_name='Name', null=True)
    value = pw.TextField(column_name='value', null=False)

    class Meta:
        table_name = 'Var'


Var.create_table()

