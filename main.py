import discord
from discord import app_commands
from discord.ui import Button, View
from discord.colour import Colour
from buttons import HitButton


import sqlite3
from dotenv import dotenv_values

TOKEN = dotenv_values(".env")["TOKEN"]

# Intents are the events that are listened for
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Holds the slash commands
command_tree = app_commands.CommandTree(client=client)

# Dict of players and their games
games = {}

# @ Symbol means decorator, in this case, the client.event decorator function
# Essentially, registers an event for the client object to listen to.
# check the github for code, or setattr to understand.
@client.event
async def on_ready():
    # Sync up all slash commands before starting up
    await command_tree.sync()
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send("HELLO")

@command_tree.command(name="say_hi")
async def hi(interact: discord.Interaction):
    reply = interact.response
    embed = discord.Embed(title="This is an embedded response", color=Colour.blue(), description="This is the description")
    player = interact.user.id

    if player in games.keys():
        embed.title = "Finish previous game"
        await reply.send_message(embed=embed)
    else:
        games[player] = interact.id
        buttons = View()
        buttons.add_item(HitButton())
        buttons.add_item(item=Button(label="Bye"))
        await reply.send_message(embed=embed, view=buttons)


client.run(TOKEN)