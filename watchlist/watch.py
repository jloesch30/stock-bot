import datetime
from database.crud import getUser, updateWatchList, getWatchList
from tickRequests.ticker import validateTickers, getTickerPrice
from scrape.finviz import finvizReport


class WatchResponse():
    def __init__(self, dateTime=None, userName=None, res=None, embed=False):
        self.userName = userName
        self.res = res  # this will be a string that is sent
        self.dateTime = dateTime
        self.embed = embed


def watchCall(msg_content, user_id, username):
    options = ['price', 'news', 'add', 'remove',
               'list']  # TODO: impliment options
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
        for i in range(len(msg_lst)):
            if ',' in msg_lst[i]:
                msg_lst[i] = msg_lst[i].replace(',', '')
        tickers = msg_lst[2:]
        res, tick = validateTickers(tickers)

        # one of the tickers DNE
        if not res:
            print('Ticker DNE in the validateTickers call')
            new_watch_obj.res = f"ticker {tick} DNE, please make sure the spelling is correct. For Cypto, you must include the currency (ex. -USD)"
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
        s = f'Ticker prices for {username}:\n'
        for tick in tickers:
            p = getTickerPrice(tick)
            s += f'{tick}: {p}\n'

        new_watch_obj.res = s
        return new_watch_obj

    elif option == 'list':
        s = f'Tickers for {username}:\n'
        tickers = getWatchList(db_user)
        for tick in tickers:
            s += tick + '\n'

        new_watch_obj.res = s

        return new_watch_obj

    elif option == 'news':
        tickers = getWatchList(db_user)
        embed_dict = finvizReport(tickers)
        new_watch_obj.res = embed_dict
        new_watch_obj.embed = True
        return new_watch_obj
        