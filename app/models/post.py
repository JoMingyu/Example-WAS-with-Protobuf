from peewee import *

from app.extensions import db
from app.models import BaseModel


class TblPosts(BaseModel):
    content = CharField(max_length=4095)

    class Meta:
        database = db
        table_name = 'tbl_posts'
