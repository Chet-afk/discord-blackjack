from cards import Card, Deck





class Blackjack():
    def __init__(self):
        self._full_deck = Deck()
        self._player_hand = []
        self._dealer_hand = []
        self._state = "Player"

        self.start()

    def start(self):
        # Start of the game, deal cards
        for i in range(2):
            self.draw_player()
            self.draw_dealer()

    def draw_player(self):
        self._player_hand.append(self._full_deck.draw())
        if not self.end_check():
            return self.end_check()


    def draw_dealer(self):
        self._dealer_hand.append(self._full_deck.draw())

    def stand(self):
        while self.get_dealer_val() < 17:
            self.draw_dealer()

    # 1 means player won, 2 means push, 0 means loss
    def end_check(self)->int:
        if self.get_player_val() > 21 or (self.get_player_val() < self.get_dealer_val() and self._state != "Player"):
            return 0
        elif self.get_player_val() == self.get_dealer_val():
            return 2
        else:
            return 1

    def get_player_val(self)->int:
        total = 0

        for card in self._player_hand:

            # Check if Ace can be considered 11
            if card.get_label() == "A":
                if total + 11 > 21 and total + 1 <= 21:
                    total += 1
                else:
                    total += 11
            else:
                total += card.get_value()

        return total

    def get_dealer_val(self)->int:
        total = 0

        for card in self._dealer_hand:

            # Check if Ace can be considered 11
            if card.get_label() == "A":
                if total + 11 > 21 and total + 1 <= 21:
                    total += 1
                else:
                    total += 11
            else:
                total += card.get_value()

        return total

if __name__ == "__main__":
    game = Blackjack()
    print(f"player hand val: {game.get_player_val()}, dealer hand val: {game.get_dealer_val()}")
    game.stand()
    print(f"player hand val: {game.get_player_val()}, dealer hand val: {game.get_dealer_val()}")