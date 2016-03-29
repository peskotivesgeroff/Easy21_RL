from easy21_mgr import EasyDealer
import numpy as np

def step(state, action, dealer):
    player_sum = state % 21 + 1
    if action == 'stick':
        new_state = 210
        dealer_sum = dealer.start_dealer_turns()
        if dealer_sum > 21 or dealer_sum < 1 or player_sum > dealer_sum:
            reward = 1
        elif player_sum < dealer_sum:
            reward = -1
        else:
            reward = 0
    else:
        new_card = dealer.deal()
        old_player_sum = player_sum
        if new_card.suite == 'red':
            player_sum -= new_card.rank
            print('you got a red %i' % new_card.rank)
        else:
            player_sum += new_card.rank
            print('you got a black %i' % new_card.rank)

        if player_sum > 21 or player_sum < 1:
            reward = -1
            new_state = 210
        else:
            reward = 0
            new_state = state + (player_sum - old_player_sum)
    return reward, new_state

def main():
    dealer = EasyDealer()
    while True:
        dealer_showing = dealer.start_game()
        first_black = dealer.deal_black()
        print('dealer showing: %i' % dealer_showing)
        print('you got a black %i' % first_black.rank)
        state = 21 * (dealer_showing - 1) + (first_black.rank - 1)
        #f_value = np.zeros(210)
        while True:
            action = input('Enter action:')
            if action == 'h':
                reward, state = step(state, 'hit', dealer)
            else:
                reward, state = step(state, 'stick', dealer)
            if state == 210:
                print('you got a reward %i' % reward)
                break

if __name__ == '__main__':
    main()
