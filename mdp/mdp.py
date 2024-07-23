"""
This file contains the `MDP` class for representing Markov Decision Processes.
The class implements the Value Iteration algorithm for solving such problems,
producing its utility map and optimal policy.
"""


class MDP:
    """
    Markov decision process.
    """

    def __init__(self, states, gamma=0.99):
        """
        Input:
            > 'states' - list of states.
            > 'gamma' - the discount factor.
        """
        self.states = states
        self.gamma = gamma
        self.utility = {state: 0 for state in self.states}
        self.policy = None

    def bellmanUpdate(self):
        """
        Performs a Bellman update.
        Returns the old utility dictionary and the new utility dictionary.
        """
        newUtility = {}  # to hold the new utilities
        oldUtility = self.utility

        # update utilities (17.6) in AIMA 3rd Edition
        for s in self.states:
            newUtility[s] = s.getReward() + self.gamma * \
                            max([sum([s.getOutcomeProb(a, s_tag) * oldUtility[
                                s_tag]
                                      for s_tag in s.getOutcomes(a)])
                                 for a in s.getActions()])

        self.utility = newUtility

        return oldUtility, newUtility

    def valueIteration(self, eps):
        """
        Updates the utlities according to VI alogirthm (Figure 17.4 in AIMA 3rd
        Edition) according to the given epsilon hyperparameter.
        Returns the number of Bellman updates performed.
        """
        delta = float('inf')
        iterations = 0
        while delta >= eps * (1 - self.gamma) / self.gamma:
            iterations += 1
            oldUtility, newUtility = self.bellmanUpdate();
            delta = max([abs(oldUtility[state] - newUtility[state])
                         for state in self.states])

        return iterations

    def calcPolicy(self):
        """
        Calculates the preferred policy according to the stored utilities.
        The policy is a dictionary of actions, indexed by states.
        """
        policy = {}  # to store the resulting policy

        for s in self.states:
            policy[s] = None

            # store best action in policy[s]
            bestExpUtility = float('-inf')
            for a in s.getActions():
                currExpUtility = sum([s.getOutcomeProb(a, s_tag) *
                                      self.utility[s_tag]
                                      for s_tag in s.getOutcomes(a)])
                if currExpUtility >= bestExpUtility:
                    bestExpUtility = currExpUtility
                    policy[s] = a

            # set the state's preffered action
            s.setPrefAction(policy[s])

        self.policy = policy

    def getPolicy(self):
        """
        Gets the policy dictionary stored.
        """
        return self.policy

    def getUtility(self):
        """
        Gets the utility dictionary stored.
        """
        return self.utility
