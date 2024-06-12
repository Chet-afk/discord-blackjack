import discord
from discord import app_commands
from ui_subclasses import GameEmbed, GameView

from blackjack import Blackjack as bj

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

#TODO
# Perhaps change this to the "on_raw_message_edit" to give an indication when to clear the
# active games dict
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send("HELLO")

@command_tree.command(name="blackjack")
async def Blackjack(interact: discord.Interaction):

    reply = interact.response
    player = interact.user.id

    if player in games.keys():
        await reply.send_message(embed=discord.Embed(title="Please finish previous game"),
                                 ephemeral=True,delete_after=4)
    else:

        game = bj()
        embed = GameEmbed(interact.user.name, game=game)

        games[player] = interact.id

        buttons = GameView(instance=game,window=embed)

        await reply.send_message(embed=embed, view=buttons)


client.run(TOKEN)