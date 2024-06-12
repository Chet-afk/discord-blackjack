from discord import Interaction
from discord.ui.button import Button, ButtonStyle
from blackjack import Blackjack
class HitButton(Button):
    def __init__(self, game_instance: Blackjack):
        super().__init__(label="Hit", style=ButtonStyle.green)
        self._instance = game_instance


    async def callback(self, press: Interaction):

        await press.response.edit_message(view=None)