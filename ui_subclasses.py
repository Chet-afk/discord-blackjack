from discord import Interaction, Embed
from discord.ui.button import Button, ButtonStyle
from discord.ui import View
from discord.colour import Colour

from blackjack import Blackjack

class GameEmbed(Embed):
    # The embed window is where the game visuals are located.
    def __init__(self, player_name: str, game: Blackjack):
        super().__init__(title="Blackjack",
                         color=Colour.blue(),
                         description=f"Player: {player_name}")

        self._player = player_name

        self.insert_field_at(index=0, name=f"{self._player} | {game.get_player_val()}",
                             value=game.get_player_hand(),inline=False)

        self.insert_field_at(index=1, name=f"Dealer | {game.get_dealer_val()}",
                             value=game.get_dealer_hand(),inline=False)

    def change_player_info(self, total: int, cards: str):
        self.set_field_at(index=0, name=f"{self._player} | {total}", value=cards, inline=False)
    def change_dealer_info(self, total: int, cards: str):
        self.set_field_at(index=1, name=f"Dealer | {total}", value=cards, inline=False)

class GameView(View):

    # The object that holds all the buttons in an action row
    def __init__(self, instance: Blackjack, window: GameEmbed):
        super().__init__()
        self.add_item(HitButton(game_instance=instance, embed_window=window))
        self.add_item(StandButton(game_instance=instance, embed_window=window))

    def loss(self):
        self.clear_items()



# Buttons for specific user interactions
# They each hold the game instance and the embed window
# to easily edit / make calls to the game instance
class HitButton(Button):
    def __init__(self, game_instance: Blackjack, embed_window: GameEmbed):
        super().__init__(label="Hit", style=ButtonStyle.green)
        self._instance = game_instance
        self._window = embed_window
    async def callback(self, press: Interaction):

        self._instance.draw_player()
        self._window.change_player_info(total=self._instance.get_player_val(), cards=self._instance.get_player_hand())

        # Recall a 0 is returned when 21+ is drawn
        state = self._instance.in_play()
        if not state:
            if self._instance.get_player_val() == 21:
                self._instance.stand()
                self._window.change_dealer_info(total=self._instance.get_dealer_val(),
                                                cards=self._instance.get_dealer_hand())

            content = self._instance.end_game()
            await press.response.edit_message(content=content,embed=self._window, view=None)

        else:
            await press.response.edit_message(embed=self._window)

class StandButton(Button):
    def __init__(self, game_instance: Blackjack, embed_window: GameEmbed):
        super().__init__(label="Stand", style=ButtonStyle.gray)
        self._instance = game_instance
        self._window = embed_window
    async def callback(self, press: Interaction):

        self._instance.stand()
        self._window.change_dealer_info(total=self._instance.get_dealer_val(),
                                        cards=self._instance.get_dealer_hand())
        content = self._instance.end_game()
        await press.response.edit_message(content=content, embed=self._window, view=None)

