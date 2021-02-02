from . import db
from mongoengine import DoesNotExist
from mongoengine import *

# ----------------
# document imports
# ----------------
from database.docs import User, WatchList

def gettWatchMorning(db_user):
    pass

def getWatchAfternoon(db_user):
    pass

def getWatchList(db_user):
    return db_user.

def getWatchPrice(db_user):
    pass

def getWatchNews(db_user):
    pass

def updateWatchList(db_user, option, tikers=None):
    pass

def getUser(user_id):
    try:
        db_user = User.objects(u_id=user_id)
    except DoesNotExist as e:
        print('User DNE')
        print('Creating user')
        return -1
    else:
        return db_user

def createUser(user_id):
    new_watch_list = WatchList()
    new_user = User(
        u_id=user_id,
        watch_list=new_watch_list
    )
    new_watch_list.user = new_user
    
    new_user.save()
    new_watch_list.save()