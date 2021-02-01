from ..stockBot import db
from mongoengine import DoesNotExist
from mongoengine import *

# ----------------
# document imports
# ----------------
from database.docs import User, WatchList

def postWatchMorning():
    pass

def postWatchAfternoon():
    pass

def getWatchList(db_user):
    pass

def getUser(user_id):
    try:
        db_user = User.objects(u_id=user_id)
    except DoesNotExist as e:
        print('User DNE')
        print('Creating user')
        createUser(user_id)

def createUser(user_id):
    new_user = User(
        u_id=user_id
    )