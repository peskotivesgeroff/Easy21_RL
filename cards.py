from random import choice

class Card():
    def __init__(self, card_idx):
        self.rank = card_idx % 10 + 1
        suite_idx = int(card_idx / 10)
        switcher = {
                0: 'red',
                1: 'black',
                2: 'black',
        }
        self.suite = switcher[suite_idx]

class CardDeck():
    def __init__(self):
        self.cards = []
        for i in range(30):
            self.cards.append(Card(i))

    def deal_black(self):
        return choice(self.cards[10:30])

    def deal(self):
        return choice(self.cards)
