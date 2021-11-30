# A class that takes actions and translates
# them into input handling, for movement
# and hotkeys, for example

from typing import Optional
import tcod.event
from Action import *
from Screens import ALPHA_INPUT

class EventHandler(tcod.event.EventDispatch[Action]):
    
    def __init__(self, game_loop) -> None:
        super().__init__()
        self.game_loop = game_loop
    
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        """Checks if the event calls for the exiting of the game process"""
        raise SystemExit()
    
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        """Checks if a key is down and acts appropriately"""        
        action: Optional[Action] = None
        key = event.sym

        # Check if the game loop is in a text receive state
        textLock = False
        if self.game_loop != None:
            textLock = self.game_loop.textLock        

        if textLock: # If the text lock is on, then only these inputs are allowed
            if key in ALPHA_INPUT:
                action = TextKeyPress(ALPHA_INPUT[key])
            elif key == tcod.event.K_RETURN:
                action = EnterAction()
        elif key == tcod.event.K_UP or key == tcod.event.K_w:
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
        elif key == tcod.event.K_q: # Potion Key
            action = UsePotion()
        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()
        elif key == tcod.event.K_F1:
            action = ToolTipUI()
        
        return action
    