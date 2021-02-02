import datetime
from database.crud import getUser, updateWatchList, getWatchList

class WatchResponse():
    def __init__(self, dateTime=None, userName=None, res=None):
        self.userName = userName
        self.res = res # this will be a string that is sent
        self.dateTime = dateTime

def watchCall(msg_content, user_id, username):
    options = ['price', 'news', 'add', 'remove'] # TODO: impliment options
    msg_lst = msg_content.split(' ')
    db_user = getUser(user_id)
    if db_user == -1:
        return 'userDNE'

    new_watch_obj = WatchResponse()
    try:
        option = msg_lst[1]
    except IndexError:
        return 'error'

    if option == 'add' or option == 'remove':
        for i in len(msg_lst):
            if ',' in msg_lst[i]:
                msg_lst[i] = msg_lst[i].replace(',', '')
        tickers = msg_lst[2:]
        print('tickers are being added:', tickers)
        updateWatchList(db_user, option, tickers)
        new_watch_obj.res = f"Tickers updated for {username}"
        return new_watch_obj
    elif option =='price':
        res = getWatchList(db_user)
        new_watch_obj.res = res
        return new_watch_obj
    
    