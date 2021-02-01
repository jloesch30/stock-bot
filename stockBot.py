import discord
import os
from dotenv import load_dotenv
from mongoengine import connect

# --------------
# module imports
# --------------
from tick_requests.ticker import get_ticker
from watchlist.watch import watchCall

# -----------------
# discord bot setep
# -----------------
client = discord.Client()

# ----------
# db connect
# ----------
db = connect('stock-bot-db', host=os.getenv('DB_CONNECT_URL'))

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
        watch_obj = watchCall(msg_content, user_id)
        await channel.send(watch_obj.res)

def main():
    # load .env
    load_dotenv()
    # login bot
    token = os.getenv("CLIENT_TOKEN")
    client.run(str(token))

if __name__ == "__main__":
    main()

