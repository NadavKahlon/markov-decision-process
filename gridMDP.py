'''
Author: Nadav Kahlon.
'''

from state import State
from MDP import MDP
import sys
from direction import directions, NoOp, getPerpDirections, directionToString


'''
A grid-traversing MDP.
'''
class GridMDP(MDP):
    '''
    Constants used by the MDP
    '''
    
    # the probability in which an action's outcome is its intended direction
    CORRECT_OUTCOME_PROB = 0.8
    # the probability in which an action's outcome is a specific direction
    # perpendicular to the intended direcition
    PERP_OUTCOME_PROB = 0.1
    
    # the default reward for a regular state
    DEFAULT_REWARD = -1
    
    # a global state for after getting to a terminal state
    ENDED_STATE = State(ID=(-1,-1), reward=0)
    ENDED_STATE.addAction(NoOp, {ENDED_STATE: 1.0})
    
    '''
    Input:
        > 'height' & 'width' - dimensions of the grid.
        > 'gamma' - the discount factor.
    '''
    def __init__(self, height, width, gamma=0.99):
        # store dimensions
        self.height = height
        self.width = width
        
        # fill a matrix of new states, and record all states in 'states'
        self.stateGrid = []
        slotStates = []
        for i in range(height):
            self.stateGrid.append([])
            for j in range(width):
                self.stateGrid[i].append(State(ID=(i,j),
                              reward=GridMDP.DEFAULT_REWARD))
                slotStates.append(self.stateGrid[i][j])
        
                
        # use 'states' in the MDP constructor
        super().__init__(slotStates + [GridMDP.ENDED_STATE], gamma)
        
        # set possible action for each state
        for state in slotStates:
            self.setSlotActions(state)
    
    '''
    Crops coordinates on the grid to valid coordinates.
    '''
    def cropCords(self, i, j):
        i = min(max(0, i), self.height-1)
        j = min(max(0, j), self.width-1)
        return i, j
        
    '''
    Sets the actions for a slot state.
    '''
    def setSlotActions(self, state):
        # get coordinates of the state on the grid
        i, j = state.getID()
        
        # each direction is one action
        for direction in directions:
            outcomes = {} # the outcomes dictionary
            
            # store "correct" outcome
            next_i, next_j = self.cropCords(i + direction[0][0],
                                            j + direction[0][1])
            outcomes[self.stateGrid[next_i][next_j]] = GridMDP.CORRECT_OUTCOME_PROB
            
            # store "incorrect" outcomes
            for perpDirection in getPerpDirections(direction):
                next_i, next_j = self.cropCords(i + perpDirection[0][0],
                                                j + perpDirection[0][1])
                outcome = self.stateGrid[next_i][next_j]
                if outcome not in outcomes.keys():
                    outcomes[outcome] = 0
                outcomes[outcome] += GridMDP.PERP_OUTCOME_PROB
            
            state.addAction(direction, outcomes)
    
    '''
    Sets the reward of a specific slot in the grid.
    '''
    def setReward(self, i, j, reward):
        self.stateGrid[i][j].setReward(reward)
        
    '''
    Sets a specific slot in the grid as terminal.
    '''
    def setTerminal(self, i, j):
        self.stateGrid[i][j].setActions({NoOp: {GridMDP.ENDED_STATE: 1.0}})
    
    '''
    Gets the policy in a form of a grid.
    '''
    def getPolicy(self):
        # get the policy dictionary from the super class
        policyDict = super().getPolicy()
        
        # store the policy in a matrix
        policyMat = []
        for i in range(self.height):
            policyMat.append([])
            for j in range(self.width):
                policyMat[i].append(policyDict[self.stateGrid[i][j]])
        
        return policyMat
    
    '''
    Gets the utility in a form of a grid.
    '''
    def getUtility(self):
        # get the policy dictionary from the super class
        utilityDict = super().getUtility()
        
        # store the policy in a matrix
        utilityMap = []
        for i in range(self.height):
            utilityMap.append([])
            for j in range(self.width):
                utilityMap[i].append(utilityDict[self.stateGrid[i][j]])
        
        return utilityMap
    
    '''
    Get the rewards of all state in a form of a grid.
    '''
    def getRewardMap(self):
        rewardMap = []
        for i in range(self.height):
            rewardMap.append([])
            for j in range(self.width):
                rewardMap[i].append(self.stateGrid[i][j].getReward())
        return rewardMap
        

'''
Main program: runs question  17.8 of AIMA 3rd Edition with an 'r' specified
    by the command line argument.
'''
if __name__ == '__main__':
    
    # get 'r' from the command line
    if len(sys.argv) != 2:
        print('Usage: gridMDP.py r')
        sys.exit(2)
    r = float(sys.argv[1])
    
    # create a 3x3 grid MDP probelem
    print(f'Creating problem with r={r}...', end=' ')
    gamma = 0.99
    problem = GridMDP(height=3, width=3, gamma=gamma)
    
    # set the terminal state
    problem.setTerminal(0,2)
    problem.setReward(0,2,  10)
    
    # set the "r" state
    problem.setReward(0,0, r)
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
    