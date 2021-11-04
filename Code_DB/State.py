# States for the Finite state machine
# Used to process moves based on the states available.
# Not super in-depth as most entities will only have basic behaviors

import random
from MathFun import *

class State:
    """ Base class for all states. Should not be called directly """
    def __init__(self, state, FSM_engine):
        self.state_ID = state
        self.turnsInState = 5 # Default for now
        self.elapsedTurns = 0 # Elapsed turns should always start at 0
        self.targetDest = Vec2(0, 0)
        self.path = []
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
        """ Determine what state to use based on choices available """
        if self.engine.actor.CanSeeTarget(self.engine.prey.Position()):
            return 'Chase'
        if self.elapsedTurns >= self.turnsInState:
            return 'Wander'
        return super().ChooseState()

    def LoadIntoState(self):
        """ What to do when returning to this state """
        super().LoadIntoState()
        self.turnsInState = random.randint(3, 10) # wait 3 to 10 turns before moving again
    
    def StateAction(self):
        """ Determines the action to take in a state """
        super().StateAction()

class Wander(State):
    """ Wandering State; Mostly aimless, may modify later. """
    def __init__(self, behavior_engine):
        super().__init__('Wander', behavior_engine)

    def ChooseState(self):
        """ Determine what state to use based on choices available """
        if self.engine.actor.CanSeeTarget(self.engine.prey.Position()):
            return 'Chase'
        if self.elapsedTurns >= self.turnsInState:
            self.elapsedTurns = 0
            return 'Idle'
        return super().ChooseState()
    
    def LoadIntoState(self):
        """ What to do when returning to this state """
        super().LoadIntoState()
        self.turnsInState = random.randint(5, 15)
    
    def StateAction(self):
        """ Determines the action to take in a state """
        super().StateAction()
        move_dir = Vec2(0, 0)
        direction = random.randint(0, 3)
        if direction == 0:
            move_dir.x += 1
        elif direction == 1:
            move_dir.y += 1
        elif direction == 2:
            move_dir.x -= 1
        elif direction == 3:
            move_dir.y -= 1
        self.engine.actor.Move(move_dir)

class Chase(State):
    """ Found its prey (typically player), moving toward it now """
    def __init__(self, FSM_engine):
        super().__init__('Chase', FSM_engine)

    def ChooseState(self):
        """ Determine what state to use based on choices available """
        if self.path == []:
            self.engine.SendMessage(self.engine.actor.name + ' has lost the player. Returning to idle.')
            return 'Idle' # Lost player, take a break
        return super().ChooseState()
    
    def LoadIntoState(self):
        """ What to do when returning to this state """
        super().LoadIntoState()
        self.targetDest = self.engine.GetPreyLocation()
        self.path = self.engine.GetPath(self.targetDest)

    def StateAction(self):
        """ Determines the action to take in a state """
        super().StateAction()
        self.targetDest = self.engine.GetPreyLocation()
        if self.engine.actor.CanSeeTarget(self.targetDest):
            self.path = self.engine.GetPath(self.targetDest)
        
        # Next move
        if len(self.path) > 0:
            move = self.path.pop(0)
            move_dir = Vec2(0, 0)
            startPos = self.engine.actor.Position()
            if move.x > startPos.x:
                move_dir.x += 1
            elif move.x < startPos.x:
                move_dir.x -= 1
            elif move.y > startPos.y:
                move_dir.y += 1
            elif move.y < startPos.y:
                move_dir.y -= 1

            self.engine.actor.Move(move_dir)