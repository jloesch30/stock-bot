import discord
import os
import time
from asyncio import TimeoutError
from dotenv import load_dotenv
import discord

# --------------
# module imports
# --------------
from watchlist.watch import watchCall
from tickRequests.ticker import getTicker
from database.crud import createUser
from sched.dailyReport import run_continuously
from database.docs import User, WatchList
from scrape.finviz import finvizReport

# ---------
# functions
# ---------

client = discord.Client()


@client.event
async def on_ready():
    print(f"bot is ready, logged in as {client.user}")


@client.event
async def on_message(message):
    channel = message.channel
    if message.content.startswith('$stock'):
        msg_content = message.content
        try:
            response = getTicker(msg_content)
            if response == -1:
                raise Exception
            if response.option == 'price':
                await channel.send(f"{response.res.get('ticker')}: {response.res.get('ask')}")
            elif response.option == 'desc':
                await channel.send(
                    f"Name: {response.res.get('shortName')}\nSector: {response.res.get('sector')}\nOpen: {response.res.get('open')}\nDay Low: {response.res.get('dayLow')}\nDay High: {response.res.get('dayHigh')}\nWebsite: {response.res.get('website')}"
                )
            elif response.option == 'high':
                await channel.send(f"Day High for {(response.res.get('ticker')).upper()}: {response.res.get('dayHigh')}")
            elif response.option == 'low':
                await channel.send(f"Day Low for {(response.res.get('ticker')).upper()}: {response.res.get('dayLow')}")
        except Exception as e:
            print(e)
            await channel.send("Sorry, that command was invalid")
            return

    elif message.content.startswith('$watch'):
        # watch stocks
        msg_content = message.content
        user_id = message.author.id
        username = message.author
        res = watchCall(msg_content, user_id, username)
        if res == 'userDNE':
            await channel.send(f"the user {username} does not exist, would you like to make one? [y/n]")

            def check(m):
                return m.content == 'y' and m.channel == message.channel

            try:
                msg = await client.wait_for('message', check=check, timeout=30.0)
            except TimeoutError:
                await channel.send(f"❌ The user {username} was not created due to timout or decline")
            else:
                createUser(message.author.id, message.author)
                await channel.send(f"creating user for {username}, you may now add items to your watch list.")

        # successful call
        elif res != 'error':
            # TODO: admin sends all reports
            if res.admin_call == True:
                if res.res == 'all':
                    watchlists = WatchList.objects
                    for l in watchlists:
                        user = l.user
                        username = user.user_name
                        tickers = l.tickers
                        if len(tickers) != 0:
                            finvizReport(tickers)
                            # send the report
                            await channel.send(f"📈 Report for **{username}**", file=discord.File(r'./xlsxwrite/report.xlsx'))
                        else:
                            await channel.send(f"👎 User **{username}** does not have any tickers registered")
                    
                    # delete files
                    if os.path.exists(r'./xlsxwrite/report.xlsx'):
                        os.remove(r'./xlsxwrite/report.xlsx')
                    else:
                        print('The file does not exist')

            elif res.file == True:
                try:
                    await channel.send(f"📈 Report for **{username}**", file=discord.File(r'./xlsxwrite/report.xlsx'))
                    if os.path.exists(r'./xlsxwrite/report.xlsx'):
                        os.remove(r'./xlsxwrite/report.xlsx')
                    else:
                        print('The file does not exist')
                except Exception as e:
                    print(e)
                    await channel.send('💀 There was an error retrieving the report')
            else:
                await channel.send(res.res)  # send the response

        # unknown error
        else:
            await channel.send("There was an error, please make sure to keep your format such that:\n$watch <option> <tickers>")

# Start the background thread
# stop_run_continuously = run_continuously(client)


def main():
    # load .env
    load_dotenv()
    # login bot
    token = os.getenv("CLIENT_TOKEN")
    client.run("ODA1NTk3NjUwNTYwMDkwMTQz.YBdNRw.ANYo0gXiyW9G_5VTCcnQV66sGsQ")


if __name__ == "__main__":
    main()
