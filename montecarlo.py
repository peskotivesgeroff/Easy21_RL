from easy21_mgr import EasyDealer, step
import numpy as np
from random import random, randint
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import sys

def choose_action_e_greedy(dealer_showing, current_sum, epsilon, Q):
    if random() <= epsilon:
        action_idx = randint(0, 1)
    else:
        action_idx = np.argmax(Q, axis=2)[dealer_showing, current_sum]
    return action_idx


def main():
    dealer = EasyDealer()
    # the 1st dimension corresponds to dealer's showing card
    # the 2nd dimension corresponds to player's sum
    # the 3rd dimension corresponds to action A (0: hit, 1: stick)
    Q = np.zeros((10, 21, 2)) # Action-Value function
    N = np.zeros((10, 21, 2)) # N(s,a): number of times that action 'a' has been selected from state 's'
    N_s = np.zeros((10, 21)) # N(s): number of times that state 's' has been visited

    N_0 = 100
    switcher = {
        0: 'hit',
        1: 'stick'
    }
    for episode in range(10000000):
        sys.stdout.write('\r%i'%(episode+1))
        # start episode
        dealer_showing = dealer.start_game() - 1 # this sum had been subtracted by one
        current_sum = dealer.deal_black().rank - 1

        # sample an episode sequence
        state_sequence = []
        action_sequence = []
        reward = 0
        while True:
            state_idx = 21 * dealer_showing + current_sum
            N_s[dealer_showing, current_sum] += 1
            #epsilon_t = N_0/(N_0 + np.sum(N, axis=2)[dealer_showing, current_sum])
            epsilon_t = N_0/(N_0 + N_s[dealer_showing, current_sum])
            #print(epsilon_t)
            # epsilon is probability of random action, or else choose greedy action
            action_idx = choose_action_e_greedy(dealer_showing, current_sum, epsilon_t, Q)

            state_sequence.append(state_idx)
            action_sequence.append(action_idx)
            reward, new_state = step(state_idx, switcher[action_idx], dealer)

            if new_state == 210:
                break
            else:
                current_sum = new_state % 21

        # start updating
        for state, action in zip(state_sequence, action_sequence):
            dealer_showing = state / 21
            current_sum = state % 21
            N[dealer_showing, current_sum, action] += 1
            alpha_t = 1/N[dealer_showing, current_sum, action]
            Q[dealer_showing, current_sum ,action] += \
                    alpha_t * (reward - Q[dealer_showing, current_sum, action])

    # plot Value function v
    v = np.max(Q, axis=2)
    #v = Q[:,:,0]
    fig = plt.figure(1)
    ax = fig.gca(projection='3d')
    X = np.arange(1, 11)
    Y = np.arange(1, 22)
    X, Y = np.meshgrid(X, Y)
    surf = ax.plot_surface(X, Y, v.T, rstride=1, cstride=1, cmap=cm.coolwarm,
                                   linewidth=0, antialiased=False)
    ax.set_xlim(1, 10)
    ax.set_ylim(1, 21)
    ax.set_zlim(-1, 1)
    ax.zaxis.set_major_locator(LinearLocator(10))
    #ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()

    # plot Policy pi
    fig = plt.figure(2)
    pi = np.argmax(Q, axis=2)
    CS = plt.contourf(X, Y, pi.T, [0, 0.5, 1], cmap=cm.bone, origin='lower')
    cbar = plt.colorbar(CS)
    plt.show()

if __name__ == '__main__':
    main()
