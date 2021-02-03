from . import db
from mongoengine import *

# ----------------
# document imports
# ----------------
from database.docs import User, WatchList

def gettWatchMorning(db_user):
    pass

def getWatchAfternoon(db_user):
    pass

# return an array of tickers
def getWatchList(db_user):
    try:
        return db_user.watch_list.tickers
    except Exception as e:
        print(e)
        return []

def getWatchPrice(db_user):
    pass

def getWatchNews(db_user):
    pass

def updateWatchList(user_id, option, ticks):
    if option == 'add':
        for tick in ticks:
            u = User.objects(u_id=user_id)
            u.watch_list.update(push_all__tickers=ticks)
    elif option == 'remove':
        u = User.objects(u_id=user_id)
        u.watch_list.tickers.update(pull_all__tickers=ticks)
        

def getUser(user_id):
    try:
        db_user = User.objects.get(u_id=user_id)
        print(db_user)
    except Exception as e:
        print('User DNE')
        print('Creating user')
        return -1
    else:
        return db_user

def createUser(user_id):
    print(type(user_id))
    new_watch_list = WatchList()
    new_user = User(
        u_id=user_id,
        watch_list=new_watch_list
    )

    new_watch_list.save()
    new_user.save()
    

    print('user created')