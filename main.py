import discord
from discord import app_commands
from ui_subclasses import GameEmbed, GameView

from blackjack import Blackjack as bj
import database

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
    database.init_setup()

    print(f"Logged in as {client.user}")


@client.event
async def on_message_edit(prior_message: discord.Message, new_message: discord.Message):
    words = new_message.content
    # Check if the editted message was the bots,
    # and if the editted values have content (none means the game is still going
    if prior_message.author != client.user or words == "":
        return

    user = new_message.interaction.user.id
    bet = games[user][1]

    if words == "You win":
        database.update(user, bet)
    elif words == "You lose":
        database.update(user, -bet)

    del games[user]





@command_tree.command(name="blackjack")
async def Blackjack(interact: discord.Interaction, bet: int):

    reply = interact.response
    player = interact.user.id

    if not database.exists(player):
        await reply.send_message(embed=discord.Embed(title="Please use the /register command"))
        return

    if bet > database.get_chips(player):
        await reply.send_message(embed=discord.Embed(title=f"You only have {database.get_chips(player)} chips"))
        return

    if player in games.keys():
        await reply.send_message(embed=discord.Embed(title="Please finish previous game"),
                                 ephemeral=True,delete_after=4)
    else:

        game = bj()
        embed = GameEmbed(interact.user.name, game=game)
        games[player] = (game, bet)

        # Natural 21 on draw
        if game.get_player_val() == 21:
            game.stand()
            await reply.send_message(content=game.end_game(), embed=embed)
        else:
            buttons = GameView(instance=game,window=embed)
            await reply.send_message(embed=embed, view=buttons)

@command_tree.command(name="register")
async def Register(interact: discord.Interaction):
    user = interact.user.id
    if database.exists(user):
        await interact.response.send_message(embed=discord.Embed(title="You are already registered"),
                                             ephemeral=True)
    else:
        database.register(user)
        await interact.response.send_message(embed=discord.Embed(title="Successfully Registered"))

@command_tree.command(name="chips")
async def Chips(interact: discord.Interaction):
    user = interact.user.id
    if database.exists(user):
        await interact.response.send_message(embed=discord.Embed(title=f"You have: {database.get_chips(user)} chips"))

@command_tree.command(name="pity")
async def Pity(interact: discord.Interaction):
    user = interact.user.id
    if database.exists(user) and database.get_chips(user) <= 500:
        await interact.response.send_message(embed=discord.Embed(title=f"You've gained 500 chips out of pity!"))
        database.update(user, 500)
    else:
        await interact.response.send_message(embed=discord.Embed(title=f"No pity for you!"))

client.run(TOKEN)

database.close()