from mongoengine import Document
from mongoengine.fields import *
from mongoengine import CASCADE, DENY
import datetime

# example discord client id: 360766607363932161 (Vudly)

class User(Document):
    u_id = StringField(max_length=200, required=True, unique=True)
    watch_list = ReferenceField('WatchList', reverse_delete_rule=CASCADE)
    date_created = DateTimeField(default=datetime.datetime.utcnow)

class WatchList(Document):
    user = ReferenceField('User', reverse_delete_rule=CASCADE)
    tickers = ListField(field=StringField)

User.register_delete_rule(WatchList, 'user', DENY)