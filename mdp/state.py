class State:
    """
    MDP state.
    """

    def __init__(self, ID, reward=0):
        """
        Input:
            > 'ID' - the identifier of the state (can be anything).
        """

        self.ID = ID
        self.reward = reward
        self.actions = {}
        self.preferedAction = None

    def __key(self):
        """
        State identified by its ID
        """
        return self.ID

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.__key() == other.__key()

    def __neq__(self, other):
        return self.__key() != other.__key()

    def __str__(self):
        return str(self.ID)

    def getID(self):
        """
        Gets the state's identifier.
        """
        return self.ID

    def addAction(self, actionID, outcomesDict):
        """
        Adds an action.
        Outcomes should be a dictionary of probabilities, indexed by states.
        """
        self.actions[actionID] = outcomesDict

    def setActions(self, actions):
        """
        Sets the actions dictionary.
        """
        self.actions = actions

    def getActions(self):
        """
        Gets list of action names
        """
        return self.actions.keys()

    def getOutcomes(self, action):
        """
        Gets possible outcomes of 'action' from 'self'
        """
        return self.actions[action].keys()

    def getOutcomeProb(self, action, outcome):
        """
        Gets the probability to get from 'self' to 'outcome' via 'action'
        """
        return self.actions[action][outcome]

    def getReward(self):
        """
        Gets the reward of this state.
        """
        return self.reward

    def setReward(self, reward):
        """
        Sets the reward of this state.
        """
        self.reward = reward

    def getPrefAction(self):
        """
        Gets the preferred action for this state.
        """
        return self.prefferedAction

    def setPrefAction(self, prefferedAction):
        """
        Sets the preferred action of this state.
        """
        self.prefferedAction = prefferedAction
