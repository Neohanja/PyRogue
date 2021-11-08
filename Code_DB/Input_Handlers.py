# A class that takes actions and translates
# them into input handling, for movement
# and hotkeys, for example

from typing import Optional
import tcod.event
from Action import *

class EventHandler(tcod.event.EventDispatch[Action]):
    
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        """Checks if the event calls for the exiting of the game process"""
        raise SystemExit()
    
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        """Checks if a key is down and acts appropriately"""
        action: Optional[Action] = None
        key = event.sym

        if key == tcod.event.K_UP or key == tcod.event.K_w:
            action = MovementAction(dx = 0, dy = -1)
        elif key == tcod.event.K_DOWN or key == tcod.event.K_s:
            action = MovementAction(dx = 0, dy = 1)
        elif key == tcod.event.K_LEFT or key == tcod.event.K_a:
            action = MovementAction(dx = -1, dy = 0)
        elif key == tcod.event.K_RIGHT or key == tcod.event.K_d:
            action = MovementAction(dx = 1, dy = 0)
        elif key == tcod.event.K_r: # Resting
            action = MovementAction(dx = 0, dy = 0)
        elif key == tcod.event.K_i: # Examine Key
            action = ExamineAction()
        elif key == tcod.event.K_RETURN:
            action = EnterAction()
        elif key == tcod.event.K_e: # Use Key
            action = UseAction()
        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()
        
        return action
    