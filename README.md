# Discord stock-bot

### Description and uses
This bot is being created for a private server to record and display stock information

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
```
$watch add AAPL, GOLD
```
```
$watch remove AAPL, GOLD
```
```
$watch news
```
```
$watch price
```
```
$stock price AAPL
```
```
$watch desc AAPL
```
```
$watch high AAPL
```
```
$watch low AAPL
```
