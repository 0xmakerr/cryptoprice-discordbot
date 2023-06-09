import discord
from random import randint
from pyth import get_price, asyncio

TOKEN = "YOUR SECRET TOKEN"
SYMBOL = "SOL/USD"

status = discord.Status.online
intents = discord.Intents.default()
client = discord.Client(intents=intents, status=status)


async def change_nickname():
    while True:
        try:
            price = await get_price()
            for guild in client.guilds:
                try:
                    await asyncio.sleep(2) # Allows some time for the client to update its cache with the latest information
                    await guild.me.edit(nick=f"${price:.2f}")
                except discord.errors.Forbidden: # Missing Change Nickname permission
                    continue
                except discord.errors.NotFound: # Guild not found or bot is not a member of the guild
                    continue
                except OSError as e:
                    print(f"Error occurred: {e}. Retrying...")
                    await asyncio.sleep(randint(30, 90))
                except Exception as e:
                    print("Error:", e)
                    await asyncio.sleep(60)
        except ConnectionResetError:
            print("Cannot write to closing transport. Retrying...")
        await asyncio.sleep(randint(5, 10))


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    activity = discord.Activity(type=discord.ActivityType.watching, name=SYMBOL)
    await client.change_presence(activity=activity)
    client.loop.create_task(change_nickname())

client.run(TOKEN)
