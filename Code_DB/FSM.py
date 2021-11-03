# Finite State Machine for assistance with AI decision making

import State
from MathFun import *

class FSM: # Basic FSM, mostly for mindless monsters
    """ FSM Decision Processing """
    def __init__(self, my_home_map, who_am_i, keep_watch_for):
        """ Constructor """
        self.stateList = {}
        self.currentState = 'Idle' # All entites need to have an idle state
        self.lastState = 'Idle'
        self.map = my_home_map # Map.WorldMap
        self.actor = who_am_i # Actor.Monster, Actor.NPC or Actor.Player
        self.prey = keep_watch_for # aka: the target!
        self.BuildStateList()
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
                print(self.actor.name,'has switched to', self.currentState + '.')
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
        self.stateList['Chase'] = State.Chase(self)

    # Helper Functions
    def GetPreyLocation(self):
        """ Gets the location of the prey (target), returning it as a deep copy """
        return self.prey.Position()

    def GetPath(self, destination : Vec2):
        """ Returns the path from an A* Pathfinding """
        pathFinder = self.map.GetPathfinder()
        return pathFinder.FindPath(self.actor.Position(), destination, True)

# Any special cases will go down here, such as villagers with different logic or party members