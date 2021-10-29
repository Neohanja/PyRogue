# States for the Finite state machine
# Used to process moves based on the states available.
# Not super in-depth as most entities will only have basic behaviors

import random

class State:
    """ Base class for all states. Should not be called directly """
    def __init__(self, state):
        self.State_ID = state
        self.TurnsInState = 5 # Default for now
        self.ElapsedTurns = 0 # Elapsed turns should always start at 0
    
    def ChooseState(self):
        """ Determine what state to use based on choices available """
        return self.State_ID
    
    def LoadIntoState(self):
        """ What to do when returning to this state """
        self.ElapsedTurns = 0 # Reset the turns in this state
    
    def StateAction(self):
        """ Determines the action to take in a state """
        self.ElapsedTurns += 1 # Since the state processed something, always increment turns by 1

class Idle(State):
    """ An idle state, as in not moving, just waiting """
    def __init__(self):
        super().__init__('Idle')
    
    def ChooseState(self):
        return super().ChooseState()

    def LoadIntoState(self):
        super().LoadIntoState()
        self.TurnsInState = random.randint(3, 10) # wait 3 to 10 turns before moving again
    
    def StateAction(self):
        super().StateAction()    