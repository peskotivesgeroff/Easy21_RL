from cards import CardDeck

def step(state, action, dealer):
    player_sum = state % 21 + 1
    if action == 'stick':
        new_state = 210
        dealer_sum = dealer.start_dealer_turns()
        if dealer_sum > 21 or dealer_sum < 1 or player_sum > dealer_sum:
            reward = 1
            '''
            if dealer_sum > 21 or dealer_sum < 1:
                print('dealer boom')
            else:
                print('player large')
            '''
        elif player_sum < dealer_sum:
            #print('player_small')
            reward = -1
        else:
            reward = 0
    else:
        new_card = dealer.deal()
        old_player_sum = player_sum
        if new_card.suite == 'red':
            player_sum -= new_card.rank
            #print('you got a red %i' % new_card.rank)
        else:
            player_sum += new_card.rank
            #print('you got a black %i' % new_card.rank)

        if player_sum > 21 or player_sum < 1:
            #print('player boom')
            reward = -1
            new_state = 210
        else:
            reward = 0
            new_state = state + (player_sum - old_player_sum)
    return reward, new_state

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
                #print('dealer got a red %i' % new_card.rank)
            else:
                self.sum += new_card.rank
                #print('dealer got a black %i' % new_card.rank)

            if self.sum >= 17 or self.sum < 1:
                return self.sum

    def deal_black(self):
        return self.deck.deal_black()

    def deal(self):
        return self.deck.deal()
