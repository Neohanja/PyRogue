# File: Pyrog.py (Python Rogue-Esque)
# AUthor: George Hall
# CS 120 Final: Python Rogue-like mini-game

# Files included to assist with functionality
import tcod

# Self made files for classes and additional functions
from Game_Manager import GameManager
from Action import *
from Input_Handlers import *
from MathFun import *

# Constant global variables : Screen size
WIDTH, HEIGHT = 100, 60

# Declare as the main function:
def main() -> None:
    game_loop = GameManager(Vec2(WIDTH, HEIGHT), True)
    refresh_screen = True

    # Code from python-tcod.readthedocs.io/en/latest/tcod/getting-started.htlm to set up a custom screen for imporved display
    tileset = tcod.tileset.load_tilesheet(
        'terminal12x12_gs_ro.png', 16, 16,
        tcod.tileset.CHARMAP_CP437)
    console = tcod.Console(WIDTH, HEIGHT, order = "F")
    event_handler = EventHandler(game_loop)

    with tcod.context.new(
        columns=console.width,
        rows=console.height,
        tileset=tileset,
        title = "Python Rogue-Esque : Intro to Computing Finale",
        vsync = True
    ) as context:
        while True:
            
            if refresh_screen: # Since the screen does not need to be updated every frame
                console.clear()
                game_loop.Draw(console)
                context.present(console)
                refresh_screen = False

            for event in tcod.event.wait():
                context.convert_event(event)
                # Debug Log - Good for figuring out what is going on behind the scenes
                # print(event) 
                action = event_handler.dispatch(event)
                if event.type == 'WINDOWRESIZED': # If we change the size of the screen, it needs to be refreshed.
                    refresh_screen = True

                if game_loop.playState == 'Loading': # Special case
                    game_loop.Update(None)
                    refresh_screen = True
                    continue

                if action is None:
                    continue
                # Make sure the screen is only updated when needed, to avoid glitches in the screen from coninuous redraw
                refresh_screen = game_loop.Update(action)
                
# Main Function

if __name__ == '__main__':
    main()