from peewee import *

from app.extensions import db
from app.models import BaseModel


class TblUsers(BaseModel):
    id = CharField(primary_key=True)
    pw = CharField()
    name = CharField(max_length=127)

    class Meta:
        database = db
        table_name = 'tbl_users'
