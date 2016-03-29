from easy21_mgr import EasyDealer
import numpy as np
from random import random, randint
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt

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
    # the 1st dimension corresponds to dealer's showing card
    # the 2nd dimension corresponds to player's sum
    # the 3rd dimension corresponds to action A (0: hit, 1: stick)
    Q = np.zeros(10, 21, 2) # Action-Value function
    N = np.zeros(10, 21, 2) # N(s,a): number of times that action 'a' has been selected from state 's'
    N_s = np.zeros(10, 21) # N(s): number of times that state 's' has been visited

    N_0 = 100
    switcher = {
        0: 'hit',
        1: 'stick'
    }
    for episodes in range(10000):
        # start episode
        dealer_showing = dealer.start_game() - 1 # this sum had been subtracted by one
        current_sum = dealer.deal_black().rank - 1

        # sample an episode sequence
        state_sequence = []
        action_sequence = []
        reward = 0
        while True:
            state_idx = 21 * dealer_showing + current_sum
            N_s[dealer_showing][current_sum]+= 1
            epsilon_t = N_0/(N_0 + np.sum(N, axis=2)[dealer_showing][current_sum])
            # epsilon is probability of random action, or else choose greedy action
            if random() <= epsilon_t:
                action = switcher[randint(0, 1)]
            else:
                action = switcher[np.argmax(Q, axis=2)[dealer_showing][current_sum]]
            reward, new_state = step(state_idx, action, dealer)

            state_sequence.append(state_idx)
            action_sequence.append(action)

            if new_state == 210:
                break
            else:
                current_sum = new_state % 21

        # start updating
        for state, action in zip(state_sequence, action_sequence):
            dealer_showing = state / 21
            current_sum = state % 21
            N[dealer_showing][current_sum][action] += 1
            alpha_t = 1/N[dealer_showing][current_sum][action]
            Q[dealer_showing][current_sum][action] += \
                    alpha_t * (reward - Q[dealer_showing][current_sum][action])

    # plot Value function v
    v = np.max(Q, axis=2)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X = np.arange(0, 10)
    Y = np.arange(0, 21)
    X, Y = np.meshgrid(X, Y)
    surf = ax.plot_surface(X, Y, v, rstride=1, cstride=1, cmap=cm.coolwarm,
                                   linewidth=0, antialiased=False)
    ax.set_zlim(-1, 1)

    ax.zaxis.set_major_locator(LinearLocator(10))
    #ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()

if __name__ == '__main__':
    main()
