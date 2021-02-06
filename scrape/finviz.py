import pandas as pd
from bs4 import BeautifulSoup
# import matplotlib.pyplot as plt
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import HTTPError
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from nltk.downloader import download
# download('vader_lexicon')


def finvizReport(tickers):
    # perams
    print('getting report')
    n = 1
    embed_dict = {}
    found = True
    tick_404 = []
    news_tables = {}

    finviz_url = 'https://finviz.com/quote.ashx?t='

    for ticker in tickers:
        url = finviz_url + ticker
        req = Request(url=url, headers={'user-agent': 'my-app/0.0.1'})
        try:
            resp = urlopen(req)
            found = True
        except HTTPError:
            found = False
            print('bad tick:', ticker)
            tick_404.append(ticker)
        if found:
            html = BeautifulSoup(resp, features="lxml")
            news_table = html.find(id='news-table')
            print('Ticker being inserted', ticker)
            news_tables[ticker] = news_table

    # remove bad tickers
    for bad_tick in tick_404:
        tickers.remove(bad_tick)

    # retrieve inner HTML
    # try:
    body_text= ""
    for ticker in tickers:
        df = news_tables[ticker]
        df_tr = df.findAll('tr')
        embed_dict[ticker] = []
        embed_dict[ticker].append({'title': f'News for {ticker}'})
        print(embed_dict)
        body_text += f'**Recent News Headlines for {ticker}**: \n'

        for i, table_row in enumerate(df_tr):
            a_text = table_row.a.text
            a_link = table_row.a['href']
            td_text = table_row.td.text
            td_text = td_text.strip()
            body_text += f"{a_text}, ({td_text}) " + f"*[link]({a_link})*"# TODO: use an embed object here!
            if i == n-1:
                body_text += '\n'
                break

        embed_dict[ticker].append({'body_text': body_text})

    return embed_dict

    # except KeyError as e:
    #     print('error is:', e)
    #     pass

    # sentiment analysis
    # parsed_news = []

    # for file_name, news_table in news_tables.items():
    #     for x in news_table.findAll('tr'):
    #         text = x.a.get_text()
    #         date_scrape = x.td.text.split()

    #         if len(date_scrape) == 1:
    #             time = date_scrape[0]

    #         else:
    #             date = date_scrape[0]
    #             time = date_scrape[1]

    #         ticker = file_name.split('_')[0]

    #         parsed_news.append([ticker, date, time, text])

    # analyzer = SentimentIntensityAnalyzer()

    # columns = ['Ticker', 'Date', 'Time', 'Headline']
    # news = pd.DataFrame(parsed_news, columns=columns)
    # scores = news['Headline'].apply(analyzer.polarity_scores).tolist()

    # df_scores = pd.DataFrame(scores)
    # news = news.join(df_scores, rsuffix='_right')

    # news['Date'] = pd.to_datetime(news.Date).dt.date

    # unique_ticker = news['Ticker'].unique().tolist()
    # news_dict = {name: news.loc[news['Ticker'] == name]
    #              for name in unique_ticker}

    # values = []
    # for ticker in tickers:
    #     dataframe = news_dict[ticker]
    #     dataframe = dataframe.set_index('Ticker')
    #     dataframe = dataframe.drop(columns=['Headline'])
    #     print('\n')
    #     print(dataframe.head())

    #     mean = round(dataframe['compound'].mean(), 2)
    #     values.append(mean)

    # df = pd.DataFrame(list(zip(tickers, values)), columns=[
    #                   'Ticker', 'Mean Sentiment'])
    # df = df.set_index('Ticker')
    # df = df.sort_values('Mean Sentiment', ascending=False)
    # print('\n')
    # print(df)


if __name__ == "__main__":
    finvizReport()
