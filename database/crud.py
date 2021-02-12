from mongoengine import *

# ----------------
# document imports
# ----------------
from database.docs import User, WatchList

# return an array of tickers
def getWatchList(db_user):
    try:
        return db_user.watch_list.tickers
    except Exception as e:
        print(e)
        return -1

def updateWatchList(db_user, option, ticks):
    if option == 'add':
        WatchList.objects(user=db_user).update(add_to_set__tickers=ticks)
    elif option == 'remove':
        WatchList.objects(user=db_user).update(pull_all__tickers=ticks)
    elif option == 'r-all':
        user_ticks = WatchList.objects.get(user=db_user)
        tickers = user_ticks.tickers
        WatchList.objects(user=db_user).update(pull_all__tickers=tickers)

        
def getUser(user_id):
    try:
        db_user = User.objects.get(u_id=user_id)
    except Exception as e:
        print('User DNE')
        print('Creating user')
        return -1
    else:
        return db_user

def createUser(user_id, user_name):
    new_watch_list = WatchList()
    new_user = User(
        u_id=user_id,
        user_name=str(user_name),
        watch_list=new_watch_list
    )
    new_watch_list.save()
    new_user.save()
    new_watch_list.update(set__user=new_user)
    print('user created')