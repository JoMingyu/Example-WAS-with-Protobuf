from peewee import *

from app.extensions import db
from app.models import BaseModel
from app.models.user import TblUsers


class TblPosts(BaseModel):
    content = CharField(max_length=4095)
    author_id = ForeignKeyField(TblUsers, db_column='author_id', to_field='id')

    class Meta:
        database = db
        table_name = 'tbl_posts'
