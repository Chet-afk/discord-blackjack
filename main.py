import discord
from dotenv import dotenv_values

TOKEN = dotenv_values(".env")["TOKEN"]

# Intents are the events that are listened for
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


# @ Symbol means decorator, in this case, the client.event decorator function
# Essentially, registers an event for the client object to listen to.
# check the github for code, or setattr to understand.
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send("HELLO")


client.run(TOKEN)