"""
Main program: optimizes a policy for a 3X3 grid-MDP with the following reward
matrix:
    [[r, -1, +10],
     [-1, -1, -1],
     [-1, -1, -1]]
using the value-iteration algorithm, Where `r` is provided as a command line
argument.
"""
import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

from mdp.grid.direction import directionToString
from mdp.grid.grid_mdp import GridMDP


def main():
    # get 'r' from the command line
    if len(sys.argv) != 2:
        print('Usage: grid_mdp.py r')
        sys.exit(2)
    r = float(sys.argv[1])

    # create a 3x3 grid MDP probelem
    print(f'Creating problem with r={r}...', end=' ')
    gamma = 0.99
    problem = GridMDP(height=3, width=3, gamma=gamma)

    # set the terminal state
    problem.setTerminal(0, 2)
    problem.setReward(0, 2, 10)

    # set the "r" state
    problem.setReward(0, 0, r)
    print('done.')
    print()

    # print a map of the rewards of the different states
    rewardMap = problem.getRewardMap()
    print('Reward map:')
    for i in range(3):
        for j in range(3):
            print('%9d' % rewardMap[i][j], end='')
        print()
    print()

    # run value iteration
    eps = 1e-10
    print(f'Running VI with eps={eps}, gamma={gamma}...', end=' ')
    its = problem.valueIteration(eps=eps)
    problem.calcPolicy()
    utility = problem.getUtility()
    policy = problem.getPolicy()
    print('done.')
    print(f'It took {its} iterations.')
    print()

    # print utility
    print('Utility map:')
    for i in range(3):
        for j in range(3):
            print('%9.2f' % utility[i][j], end='')
        print()
    print()

    # print policy
    print('Policy:')
    for i in range(3):
        for j in range(3):
            print('%9s' % directionToString(policy[i][j]), end='')
        print()


if __name__ == '__main__':
    main()
