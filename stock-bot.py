import discord
import os
from dotenv import load_dotenv

# --------------
# module imports
# --------------
from tick_requests.ticker import get_ticker

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
            print('sending to ticker function')
            response = get_ticker(msg_content)
            if response == -1:
                raise Exception
            if response.option == 'ask':
                await channel.send(f"{response.res.get('ticker')}: {response.res.get('ask')}")
            elif response.option == 'desc':
                await channel.send(
                    f"Name: {response.res.get('shortName')}\nSector: {response.res.get('sector')}\nOpen: {response.res.get('open')}\nDay Low: {response.res.get('dayLow')}\nDay High: {response.res.get('dayHigh')}\nWebsite: {response.res.get('website')}"
                )
        except Exception as e:
            print(e)
            await channel.send("Sorry, that command was invalid")
            return
    elif message.content.startswith('$watch'):
        # watch stocks
        pass

def main():
    # load .env
    load_dotenv()
    token = os.getenv("CLIENT_TOKEN")
    # login bot
    client.run(str(token))

if __name__ == "__main__":
    main()

