'''
Author: Nadav Kahlon.
'''


'''
Markov decision problem.
'''
class MDP:
    '''
    Input:
        > 'states' - list of states.
        > 'gamma' - the discount factor.
    '''
    def __init__(self, states, gamma=0.99):
        self.states = states
        self.gamma = gamma
        self.utility = {state: 0 for state in self.states}
        self.policy = None
    
    '''
    Performs a Bellman update.
    Returns the old utility dictionary and the new utility dictionary.
    '''
    def bellmanUpdate(self):
        newUtility = {} # to hold the new utilities
        oldUtility = self.utility
        
        # update utilities (17.6) in AIMA 3rd Edition
        for s in self.states:
            newUtility[s] = s.getReward() + self.gamma * \
                max([sum([s.getOutcomeProb(a, s_tag) * oldUtility[s_tag]
                          for s_tag in s.getOutcomes(a)])
                    for a in s.getActions()])
        
        self.utility = newUtility
        
        return oldUtility, newUtility
    
    '''
    Updates the utlities according to VI alogirthm (Figure 17.4 in AIMA 3rd Edition)
        according tot he given epsilon hyper-parameter.
    Returns the number of Bellman updates performed.
    '''
    def valueIteration(self, eps):
       delta = float('inf')
       iterations = 0
       while delta >= eps * (1-self.gamma) / self.gamma:
           iterations += 1
           oldUtility, newUtility = self.bellmanUpdate();
           delta = max([abs(oldUtility[state] - newUtility[state])
                        for state in self.states])
    
       return iterations
    
    '''
    Calculates the preferred policy according to the stored utilities.
    The policy is a dictionary of actions, indexed by states.
    '''
    def calcPolicy(self):
        policy = {} # to store the resulting policy
        
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
    
    '''
    Gets the policy dictionary stored.
    '''
    def getPolicy(self):
        return self.policy
    
    '''
    Gets the utility dictionary stored.
    '''
    def getUtility(self):
        return self.utility