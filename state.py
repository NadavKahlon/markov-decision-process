'''
Author: Nadav Kahlon.
'''


"""
MDP state.
"""
class State:
    '''
    Input:
        > 'ID' - the identifier of the state (can be anything).
    '''
    def __init__(self, ID, reward=0):
        self.ID = ID
        self.reward = reward
        self.actions = {}
        self.preferedAction = None
    
    '''
    State identified by its ID
    '''
    def __key(self):
        return self.ID
    def __hash__(self):
        return hash(self.__key())
    def __eq__(self, other):
        return self.__key() == other.__key()
    def __neq__(self, other):
        return self.__key() != other.__key()
    def __str__(self):
        return str(self.ID)
    
    '''
    Gets the state's identifier.
    '''
    def getID(self):
        return self.ID
    
    '''
    Adds an action.
    Outcomes should be a dictionary of probabilities, indexed by states.
    '''
    def addAction(self, actionID, outcomesDict):
        self.actions[actionID] = outcomesDict
    
    '''
    Sets the actions dictionary.
    '''
    def setActions(self, actions):
        self.actions = actions
    
    '''
    Gets list of action names
    '''
    def getActions(self):
        return self.actions.keys()
    
    '''
    Gets possible outcomes of 'action' from 'self'
    '''
    def getOutcomes(self, action):
        return self.actions[action].keys()
    
    '''
    Gets the probability to get from 'self' to 'outcome' via 'action'
    '''
    def getOutcomeProb(self, action, outcome):
        return self.actions[action][outcome]
    
    '''
    Gets the reward of this state.
    '''
    def getReward(self):
        return self.reward
    
    '''
    Sets the reward of this state.
    '''
    def setReward(self, reward):
        self.reward = reward
    
    '''
    Gets the preferred action for this state.
    '''
    def getPrefAction(self):
        return self.prefferedAction
    
    '''
    Sets the preferred action of this state.
    '''
    def setPrefAction(self, prefferedAction):
        self.prefferedAction = prefferedAction