import datetime
from database.crud import getUser, updateWatchList, getWatchList
from tickRequests.ticker import validateTickers, getTickerPrice
from scrape.finviz import finvizReport


class WatchResponse():
    def __init__(self, dateTime=None, userName=None, res=None, file=False, admin_call=False):
        self.userName = userName
        self.res = res  # this will be a string that is sent
        self.dateTime = dateTime
        self.file = file
        self.admin_call = admin_call


def watchCall(msg_content, user_id, username):
    options = ['price', 'news', 'add', 'remove',
               'list', 'all']
    msg_lst = msg_content.split(' ')
    db_user = getUser(user_id)
    if db_user == -1:
        return 'userDNE'

    new_watch_obj = WatchResponse()
    new_watch_obj.userName = username

    try:
        option = msg_lst[1]
    except IndexError:
        return 'error'

    if option == 'add' or option == 'remove':
        _all = False

        # refine results
        tickers = msg_lst[2:]
        if len(tickers) == 1:
            item = tickers[0]
            items_lst = item.split(',')
            tickers = items_lst
        else:
            for i in range(len(tickers)):
                if ',' in tickers[i]:
                    tickers[i] = tickers[i].replace(',', '')

        # check if this is a single command
        if len(tickers) == 1:
            if tickers[0] == 'all':
                option = 'r-all'  # remove all
                _all = True

        if not _all:
            res, tick = validateTickers(tickers)
        else:
            res = True

        # one of the tickers DNE
        if not res:
            print('Ticker DNE in the validateTickers call')
            new_watch_obj.res = f"ticker {tick} DNE, please make sure the spelling is correct.\nFor Cypto, you must include the currency (ex. -USD).\nTickers must be written with a comma seperation such as:\n*AAPL, GOLD*)"
            return new_watch_obj

        # validation passed
        updateWatchList(db_user, option, tickers)
        new_watch_obj.res = f"Tickers updated for {username}"

        # final return
        return new_watch_obj

    # return price of each stock
    elif option == 'price':
        tickers = getWatchList(db_user)

        # no watch list
        if tickers == -1:
            new_watch_obj.res = f"No watch list is avaliable for user {username}"
            return new_watch_obj

        # watchlist found
        s = f'Ticker prices for **{username}**:\n'
        for tick in tickers:
            p = getTickerPrice(tick)
            s += f'{tick}: {p}\n'

        new_watch_obj.res = s
        return new_watch_obj

    elif option == 'list':
        s = f'Tickers for **{username}**:\n'
        tickers = getWatchList(db_user)
        for tick in tickers:
            s += tick + '\n'

        new_watch_obj.res = s

        return new_watch_obj

    elif option == 'news':  # send a xlms report in a message
        tickers = getWatchList(db_user)
        if len(tickers) == 0:
            new_watch_obj.res = "You do not have any tickers, please add some using ($watch add <ticker>, <ticker>, ...)"
            return new_watch_obj
        new_watch_obj.file = True
        finvizReport(tickers)  # create the report
        return new_watch_obj

    elif option == 'all':
        if db_user.admin == True:
            new_watch_obj.admin_call = True
            new_watch_obj.res = 'all'
            return new_watch_obj
        else:
            print('returning false')
            new_watch_obj.res = f"**{username}** is not an admin, please contact Vudly if this is a mistake"
            return new_watch_obj
    else:
        return 'error'
