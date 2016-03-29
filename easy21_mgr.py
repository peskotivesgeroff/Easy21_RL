from cards import CardDeck

class EasyDealer():
    def __init__(self):
        self.deck = CardDeck()

    def start_game(self):
        self.open_card = self.deck.deal_black()
        #self.cards = []
        #self.cards.append(self.open_card)
        self.sum = self.open_card.rank
        return self.sum

    def start_dealer_turns(self):
        while True:
            new_card = self.deck.deal()
            if new_card.suite == 'red':
                self.sum -= new_card.rank
                print('dealer got a red %i' % new_card.rank)
            else:
                self.sum += new_card.rank
                print('dealer got a black %i' % new_card.rank)

            if self.sum >= 17 or self.sum < 1:
                return self.sum

    def deal_black(self):
        return self.deck.deal_black()

    def deal(self):
        return self.deck.deal()
