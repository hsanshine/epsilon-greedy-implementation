import matplotlib.pyplot as plt
import random
import numpy as np

NUM_TRIALS = 10000
EPS = 0.1
BANDIT_PROBABILITIES = [0.2, 0.5, 0.75]


class Bandit:
    def __init__(self, p):
        # p : the win rate
        self.p = p
        self.p_estimate = 0  # the win rate you are estimating as you experiment
        self.N = 0  # the number of samples from this machine so far

    def pull(self):  # this is where we get the reward and it is a one or a zero
        # draw a 1 with a probability p
        return np.random.random() < self.p  # choose a number between 0 and 1 and we see if it is below p

    def update(self, x):
        self.N += 1
        self.p_estimate = (self.p_estimate + x) / self.N  # done this way because the sample mean is also probability
        # this is true because the values are either 0 or 1 and by calculating the sample mean we also calculate the
        # win rate or the Maximum Likelihood Estimate


def experiment():
    bandits = [Bandit(p) for p in BANDIT_PROBABILITIES]  # for loop returns a list of bandits
    rewards = np.zeros(NUM_TRIALS)  # returns an array of zeros with NUM_TRIALS number of elements
    num_times_explored = 0  # when you did sth random
    num_times_exploited = 0  # when you stuck to the winning option
    num_optimal = 0  # number of times you choose the actual optimal bandit during your run
    optimal_j = np.argmax(b.p for b in bandits)  # from the tuple containing the bandits we choose the one with the best
    # probability of winning and save it as the optimal choice or optimal j
    print('optimal j: ', optimal_j)

    for i in range(NUM_TRIALS):
        # use the epsilon greedy strategy to select the next bandit
        if np.random.random() < EPS:  # make a random choice
            num_times_explored += 1
            j = np.random.choice([0, 1, 2])  # we need to choose a bandit here but the get its index
        else:  # choose the optimal choice that you have found so far
            num_times_explored += 1
            j = np.argmax([b.p_estimate for b in bandits])

        if j == optimal_j:
            num_optimal += 1  # count the number of times that you actually made the optimal decision

        # now pull the arm of the bandit that you chose to play
        x = bandits[j].pull()
        # update the rewards logs to add this reward on the i-th trial
        rewards[i] = x

        # update the distribution of rewards for the bandit you just pulled, you change its win rate (sample mean here)
        bandits[j].update(x)

    # print the estimates for each bandit after your experiment
    for b in bandits:
        print('mean estimate: ', b.p_estimate)

    # print the total reward
    print('total reward earned: ', rewards.sum())  # the sum of all the rewards you got out of 10,000 possible rewards
    print('overall win rate: ', rewards.sum() / NUM_TRIALS)  # the win rate of your agent
    print('num_times_explored: ', num_times_explored)  # number of times you did sth random
    print('num_times_exploited: ', num_times_exploited)
    print('num_times selected the optimal bandit: ', num_optimal)

    # plot the results
    cummulative_rewards = np.cumsum(rewards)
    win_rates = cummulative_rewards / (np.arange(NUM_TRIALS) + 1)
    plt.plot(win_rates)
    plt.plot(np.ones(NUM_TRIALS) * np.max(BANDIT_PROBABILITIES))
    plt.show()


experiment()
