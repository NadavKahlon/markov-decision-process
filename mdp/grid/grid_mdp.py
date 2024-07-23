"""
Implementation of a "Grid-MDP" problem.
"""

from mdp.state import State
from mdp.mdp import MDP
from mdp.grid.direction import directions, NoOp, getPerpDirections


class GridMDP(MDP):
    """
    A grid-traversing MDP.
    """

    # the probability in which an action's outcome is its intended direction
    CORRECT_OUTCOME_PROB = 0.8
    # the probability in which an action's outcome is a specific direction
    # perpendicular to the intended direcition
    PERP_OUTCOME_PROB = 0.1

    # the default reward for a regular state
    DEFAULT_REWARD = -1

    # a global state for after getting to a terminal state
    ENDED_STATE = State(ID=(-1, -1), reward=0)
    ENDED_STATE.addAction(NoOp, {ENDED_STATE: 1.0})

    def __init__(self, height, width, gamma=0.99):
        """
        Input:
            > 'height' & 'width' - dimensions of the grid.
            > 'gamma' - the discount factor.
        """
        # store dimensions
        self.height = height
        self.width = width

        # fill a matrix with new states, and record all states in 'states'
        self.stateGrid = []
        slotStates = []
        for i in range(height):
            self.stateGrid.append([])
            for j in range(width):
                self.stateGrid[i].append(State(ID=(i, j),
                                               reward=GridMDP.DEFAULT_REWARD))
                slotStates.append(self.stateGrid[i][j])

        # use 'states' in the MDP constructor
        super().__init__(slotStates + [GridMDP.ENDED_STATE], gamma)

        # set possible action for each state
        for state in slotStates:
            self.setSlotActions(state)

    def cropCords(self, i, j):
        """
        Crops coordinates on the grid to valid coordinates.
        """
        i = min(max(0, i), self.height - 1)
        j = min(max(0, j), self.width - 1)
        return i, j

    def setSlotActions(self, state):
        """
        Sets the actions for a slot state.
        """
        # get coordinates of the state on the grid
        i, j = state.getID()

        # each direction is one action
        for direction in directions:
            outcomes = {}  # the outcomes dictionary

            # store "correct" outcome
            next_i, next_j = self.cropCords(i + direction[0][0],
                                            j + direction[0][1])
            outcomes[
                self.stateGrid[next_i][next_j]] = GridMDP.CORRECT_OUTCOME_PROB

            # store "incorrect" outcomes
            for perpDirection in getPerpDirections(direction):
                next_i, next_j = self.cropCords(i + perpDirection[0][0],
                                                j + perpDirection[0][1])
                outcome = self.stateGrid[next_i][next_j]
                if outcome not in outcomes.keys():
                    outcomes[outcome] = 0
                outcomes[outcome] += GridMDP.PERP_OUTCOME_PROB

            state.addAction(direction, outcomes)

    def setReward(self, i, j, reward):
        """
        Sets the reward of a specific slot in the grid.
        """
        self.stateGrid[i][j].setReward(reward)

    def setTerminal(self, i, j):
        """
        Sets a specific slot in the grid as terminal.
        """
        self.stateGrid[i][j].setActions({NoOp: {GridMDP.ENDED_STATE: 1.0}})

    def getPolicy(self):
        """
        Gets the policy in a form of a grid.
        """
        # get the policy dictionary from the super class
        policyDict = super().getPolicy()

        # store the policy in a matrix
        policyMat = []
        for i in range(self.height):
            policyMat.append([])
            for j in range(self.width):
                policyMat[i].append(policyDict[self.stateGrid[i][j]])

        return policyMat

    def getUtility(self):
        """
        Gets the utility in a form of a grid.
        """
        # get the policy dictionary from the super class
        utilityDict = super().getUtility()

        # store the policy in a matrix
        utilityMap = []
        for i in range(self.height):
            utilityMap.append([])
            for j in range(self.width):
                utilityMap[i].append(utilityDict[self.stateGrid[i][j]])

        return utilityMap

    def getRewardMap(self):
        """
        Get the rewards of all state in a form of a grid.
        """
        rewardMap = []
        for i in range(self.height):
            rewardMap.append([])
            for j in range(self.width):
                rewardMap[i].append(self.stateGrid[i][j].getReward())
        return rewardMap
