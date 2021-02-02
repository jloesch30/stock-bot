import discord
import os
from asyncio import TimeoutError
from dotenv import load_dotenv
from mongoengine import connect

# --------------
# module imports
# --------------
from watchlist.watch import watchCall
from tick_requests.ticker import get_ticker
from database.crud import createUser

# -----------------
# discord bot setep
# -----------------
client = discord.Client()

# ---------
# functions
# ---------
@client.event
async def on_ready():
    print(f"bot is ready, logged in as {client.user}")

@client.event
async def on_message(message):
    channel = message.channel
    if message.content.startswith('$stock'):
        msg_content = message.content
        try:
            response = get_ticker(msg_content)
            if response == -1:
                raise Exception
            if response.option == 'ask':
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
                return m.content == 'y'and m.channel == message.channel

            try:
                msg = await client.wait_for('message', check=check, timeout=30.0)
            except TimeoutError:
                await channel.send(f"The user {username} was not created due to timeout")
            else:
                createUser(message.author.id)
                await channel.send(f"creating user for {username}, you may now add items to your watch list.")
        elif res != 'error':
            await channel.send(res.res) # send the response
        else:
            await channel.send("There was an error, please make sure to keep your format such that:\n$watch <option> <tickers>")

def main():
    # load .env
    load_dotenv()
    # login bot
    token = os.getenv("CLIENT_TOKEN")
    client.run(str(token))

if __name__ == "__main__":
    main()
