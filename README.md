# Discord stock-bot

### Description and uses
This bot is being created for a private server to record and display stock information. The user can access various stock information such as price, highs, lows, news, etc. News for each stock is being compiled via webscraping and [Finviz](https://finviz.com/).

### features
1. stock pricing
2. stock descriptions
3. private watchlists
4. daily updates
5. mongoDB
6. sentiment analysis

### Progress
Currently in production, tags and releases will be used for changelogs and updates

### run me
This bot can be run by creating a .env file with the respected information

### how to use
**command format**:\
```$<command> <option> <OPTIONAL:tickers>```
1. **$stock**
  - price
  - desc
  - high
  - low
2. **$watch**
  - all (admins)
  - news
  - add
  - remove *all*
  - list
  
### examples
```
$watch list
```
Returns a list of tickers in the User's watchlist
```
$watch add AAPL, GOLD
```
Adds designated tickers to the User's watchlist
```
$watch remove AAPL, GOLD
```
Removes designated tickers to the User's watchlist
```
$watch news
```
Returns an xlsx document with news for valid tickers in the User's watchlist
```
$watch price
```
Returns prices for each ticker in the User's watchlist
```
$stock price AAPL
```
Returns the price for a stock written after the option 'price'
```
$stock desc AAPL
```
Returns a short description of the stock indicated such as shoet name, high, low, open, sector, and website
```
$stock high AAPL
```
Returns the day high price for the stock
```
$stock low AAPL
```
Returns the day low price for the stock
