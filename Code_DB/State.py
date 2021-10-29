# States for the Finite state machine
# Used to process moves based on the states available.
# Not super in-depth as most entities will only have basic behaviors

import random
import FSM
from MathFun import *

class State:
    """ Base class for all states. Should not be called directly """
    def __init__(self, state, FSM_engine : FSM.FSM):
        self.state_ID = state
        self.turnsInState = 5 # Default for now
        self.elapsedTurns = 0 # Elapsed turns should always start at 0
        self.targetDest = Vec2(0, 0)
        self.engine = FSM_engine
    
    def ChooseState(self):
        """ Determine what state to use based on choices available """
        return self.state_ID
    
    def LoadIntoState(self):
        """ What to do when returning to this state """
        self.elapsedTurns = 0 # Reset the turns in this state
    
    def StateAction(self):
        """ Determines the action to take in a state """
        self.elapsedTurns += 1 # Since the state processed something, always increment turns by 1

class Idle(State):
    """ An idle state, as in not moving, just waiting """
    def __init__(self, behavior_engine):
        super().__init__('Idle', behavior_engine)
    
    def ChooseState(self):
        return super().ChooseState()

    def LoadIntoState(self):
        super().LoadIntoState()
        self.turnsInState = random.randint(3, 10) # wait 3 to 10 turns before moving again
    
    def StateAction(self):
        super().StateAction()

class Wander(State):
    """ Wandering State """
    def __init__(self, behavior_engine):
        super().__init__('Wander', behavior_engine)

    def ChooseState(self):
        return super().ChooseState()
    
    def LoadIntoState(self):
        super().LoadIntoState()
    
    def StateAction(self):
        super().StateAction()