from mongoengine import Document
from mongoengine.fields import *
import datetime

# example discord client id: 360766607363932161 (Vudly)

class WatchList(Document):
    tickers = ListField()
    user = ReferenceField('User')
    date_created = DateTimeField(default=datetime.datetime.utcnow)
class User(Document):
    u_id = IntField(max_length=200, required=True, unique=True)
    user_name = StringField(max_length=200, required=True)
    watch_list = ReferenceField(WatchList)
    admin = BooleanField(default=False, required=True)
    date_created = DateTimeField(default=datetime.datetime.utcnow)
