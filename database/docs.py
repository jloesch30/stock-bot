from mongoengine import Document
from mongoengine.fields import *
from bson.objectid import ObjectId
import datetime

# example discord client id: 360766607363932161 (Vudly)

class WatchList(Document):
    tickers = ListField(field=StringField)
    date_created = DateTimeField(default=datetime.datetime.utcnow)
class User(Document):
    u_id = IntField(max_length=200, required=True, unique=True)
    watch_list = ReferenceField('WatchList')
    date_created = DateTimeField(default=datetime.datetime.utcnow)
