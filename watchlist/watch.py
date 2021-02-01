import datetime
from database.db import getUser

class WatchResponse():
    def __init__(self, dateTime=None, userName=None, res=None):
        self.userName = userName
        self.res = res # this will be a string that is sent
        self.dateTime = dateTime

def watchCall(msg_content, user_id):
    new_watch_obj = WatchResponse()
    db_user = getUser(user_id)