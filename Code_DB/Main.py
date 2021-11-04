# File: Pyrog.py (Python Rogue-Esque)
# AUthor: George Hall
# CS 120 Final: Python Rogue-like mini-game

# Files included to assist with functionality
import tcod
from Game_Manager import GameManager

# Self made files for classes and additional functions
from Action import *
from Input_Handlers import *
from MathFun import *

# Constant global variables : Screen size
WIDTH, HEIGHT = 100, 60

# Declare as the main function:
def main() -> None:
    game_loop = GameManager(Vec2(WIDTH, HEIGHT), True)
    refesh_screen = True

    # Code from python-tcod.readthedocs.io/en/latest/tcod/getting-started.htlm to set up a custom screen for imporved display
    tileset = tcod.tileset.load_tilesheet(
        'terminal12x12_gs_ro.png', 16, 16,
        tcod.tileset.CHARMAP_CP437)
    console = tcod.Console(WIDTH, HEIGHT, order = "F")
    event_handler = EventHandler()
    
    with tcod.context.new(
        columns=console.width, # + console.width // 2,
        rows=console.height, # + console.height // 2,
        tileset=tileset,
        title = "Python Rogue-Esque : Intro to Computing Finale",
        vsync = True
    ) as context:
        while True:
            
            if refesh_screen: # Since the screen does not need to be updated every frame
                console.clear()
                game_loop.Draw(console)
                context.present(console)
                refesh_screen = False

            for event in tcod.event.wait():
                context.convert_event(event)
                # Debug Log - Good for figuring out what is going on behind the scenes
                # print(event) 
                action = event_handler.dispatch(event)

                if action is None:
                    continue
                # Make sure the screen is only updated when needed, to avoid glitches in the screen from coninuous redraw
                refesh_screen = game_loop.Update(action)
                
# Main Function

if __name__ == '__main__':
    main()