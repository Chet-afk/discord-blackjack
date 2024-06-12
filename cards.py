from random import shuffle

class Card():
    def __init__(self, val: int, suit: str, label: str):
        # Clamps the value of the card
        self._value = val if val < 10 else 10
        self._suit = suit
        self._label = label

    def __str__(self):
        return(f"{self._label} of {self._suit}, Value: {self._value}")

    def get_value(self)->int:
        return self._value
    def get_suit(self)->str:
        return self._suit
    def get_label(self)->str:
        return self._label



class Deck():

    def __init__(self):
        self._cards = []
        self._suits = ["Spade", "Heart", "Club", "Diamond"]
        self._faces = {1: "A", 11: "J", 12: "Q", 13: "K"}

        self.create_deck()
        self.shuffle()

    def __str__(self):
        for card in self._cards:
            print(card)
        return (f"There are {len(self._cards)} in the deck.")

    def create_deck(self):
        self._cards.clear()

        face_vals = list(self._faces.keys())

        for val in range(1,14):
            for suit in self._suits:
                if val in face_vals:
                    self._cards.append(Card(val, suit, self._faces[val]))
                else:
                    self._cards.append(Card(val, suit, str(val)))


    def shuffle(self):
        shuffle(self._cards)

    def draw(self):
        return self._cards.pop()

if __name__ == "__main__":
    deck = Deck()
    print(deck)