from cards import Card, Deck





class Blackjack():
    def __init__(self):
        self._full_deck = Deck()
        self._player_hand = []
        self._dealer_hand = []

        # Bool to check if dealer hand should be shown
        self._reveal = False
        self.start()

    def start(self):
        # Start of the game, deal cards
        for i in range(2):
            self.draw_player()
            self.draw_dealer()

    def draw_player(self):
        self._player_hand.append(self._full_deck.draw())


    def draw_dealer(self):
        self._dealer_hand.append(self._full_deck.draw())

    def stand(self):
        self._reveal = True
        while self.get_dealer_val() < 17 and self.get_player_val() <= 21:
            self.draw_dealer()

    def end_game(self)->str:

        player = self.get_player_val()
        dealer = self.get_dealer_val()

        # Returns the string which triggers the end event in main
        if player > 21 or (dealer <= 21 and player < dealer):
            return "You lose"
        elif player > dealer or dealer > 21:
            return "You win"
        elif player == dealer:
            return "Push"

    def in_play(self)->int:
        # Simple check to see if the game is still in play
        if self.get_player_val() >= 21:
            return 0
        else:
            return 1


    def get_player_val(self)->int:
        total = 0
        aces = 0
        for card in self._player_hand:

            # Check if Ace can be considered 11
            if card.get_label() == "A":
                aces += 1
            else:
                total += card.get_value()
        # Ace values should be checked after calculating other values
        for ace in range(aces):
            if total + 11 <= 21:
                total += 11
            elif total + 1 <= 21:
                total += 1
            else:
                total +=1
        return total
    def get_player_hand(self)->str:
        cards = []
        for card in self._player_hand:
            cards.append(card.get_label())
        return " ".join(cards)
    def get_dealer_val(self)->int:
        total = 0
        aces = 0
        hand = self._dealer_hand

        if not self._reveal:
            # Edge case for Ace on first draw
            return hand[0].get_value() if hand[0].get_label() != "A" else 11

        for card in hand:
            if card.get_label() == "A":
                aces += 1
            else:
                total += card.get_value()

        # Ace values should be checked after calculating other values
        for ace in range(aces):
            if total + 11 <= 21:
                total += 11
            elif total + 1 <= 21:
                total += 1
            else:
                total +=1

        return total

    def get_dealer_hand(self)->str:
        cards = []
        hand = self._dealer_hand

        if not self._reveal:
            return f"{hand[0].get_label()} ?"

        for card in hand:
            cards.append(card.get_label())
        return " ".join(cards)


if __name__ == "__main__":
    game = Blackjack()
    print(f"player hand val: {game.get_player_hand()}, dealer hand val: {game.get_dealer_hand()}")
    game.stand()
    print(f"player hand val: {game.get_player_val()}, dealer hand val: {game.get_dealer_val()}")