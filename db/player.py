import peewee as pw
from db import DbModel, Rights
from datetime import datetime


class Player(DbModel):
    id = pw.AutoField(column_name='id')
    name = pw.TextField(column_name='name', null=True)
    chat_id = pw.IntegerField(column_name='chat_id', null=True)
    rights = pw.IntegerField(column_name="rights")
    move_duration = pw.IntegerField(column_name='move_duration', default=10)
    current_location = pw.IntegerField(column_name='current_location', null=True)
    home_address = pw.IntegerField(column_name="home_address", null=True)
    coming_from = pw.IntegerField(column_name="coming_from", null=True)
    busy_until = pw.TimestampField(column_name="busy_until", null=datetime.now())
    roll_target = pw.IntegerField(column_name='roll_target', null=True)
    roll_status = pw.IntegerField(column_name='roll_status', null=True)
    roll_dices = pw.TextField(column_name='roll_dices', null=True)


    class Meta:
        table_name = 'Player'

    def has_right(self, right: Rights) -> bool:
        return self.rights & right.value > 0

    def add_right(self, right: Rights) -> bool:
        if right is right.ALL:
            return False
        self.rights |= right.value
        self.save()
        return True

    def remove_right(self, right: Rights) -> bool:
        self.rights &= ~right.value
        self.save()
        return True




Player.create_table()