# Finite State Machine for assistance with AI decision making

import Map
import Actor
import State
from MathFun import *

class FSM: # Basic FSM, mostly for mindless monsters
    """ FSM Decision Processing """
    def __init__(self, my_home_map : Map.WorldMap, who_am_i : Actor):
        """ Constructor """
        self.stateList = {}
        self.currentState = 'Idle' # All entites need to have an idle state
        self.lastState = 'Idle'
        self.map = my_home_map
        self.actor = who_am_i
        pass
    
    def Update(self):
        """ Per turn update for FSM list """
        # Determine the next choice based on decision logic
        self.currentState = self.stateList[self.currentState].ChooseState()

        # If we are changing states, we need to make sure the new state is ready for us
        if self.currentState != self.lastState:
            # Check if the new state is in the state list
            if self.currentState in self.stateList:
                self.lastState = self.currentState
            else:
                print(self.currentState, 'not loaded into state list. Reverting back to', self.lastState, 'state.')
                self.currentState = self.lastState
            # Even if it is not, we still need to treat the old state like a new state, or it will switch
            # to the invalid state each turn (unless its logic says otherwise)
            self.stateList[self.currentState].LoadIntoState()

        # Conduct the activity based on the current state
        self.stateList[self.currentState].StateAction()


    def BuildStateList(self):
        """ Builds the State List """
        self.stateList['Idle'] = State.Idle(self)
        self.stateList['Wander'] = State.Wander(self)

    # Helper Functions
    def GetPath(self, destination : Vec2):
        """ Returns the path from an A* Pathfinding """

# Any special cases will go down here, such as villagers with different logic or party members