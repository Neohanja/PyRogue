# File: Pyrog.py (Python Rogue-Esque)
# AUthor: George Hall
# CS 120 Final: Python Rogue-like mini-game

# Files included to assist with functionality
import tcod

# Self made files for classes and additional functions
import Screens
from Action import *
from Input_Handlers import *
from Map import *
from MathFun import *
from AIManager import *

# Constant global variables
WIDTH, HEIGHT = 100, 60
WORLD_SIZE = 256

# Declare as the main function:
def main() -> None:
    # Build the world
    world = WorldMap(WORLD_SIZE, WORLD_SIZE)
    world.BuildOverworld()
    # Initialize the AI Management system
    actor_manager = AI_Manager(world)
    actor_manager.ToggleDebug(True)
    
    # Declaration of local variables
    eAction = ''
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
                border = Screens.WorldUI(WIDTH, HEIGHT)
                for line in range(len(border)):
                    console.print(x=0,y=line, string = border[line])
            
                # Determine the upper left corner of the map for draw screen
                map_corner = Vec2(
                    Clamp(0, world.width - WorldMap.MAP_VIEW_WIDTH + 1, actor_manager.player.position.x - (WorldMap.MAP_VIEW_WIDTH // 2)),
                    Clamp(0, world.height - WorldMap.MAP_VIEW_HEIGHT + 1, actor_manager.player.position.y - (WorldMap.MAP_VIEW_HEIGHT // 2)))

                # Draw the map first
                world.Draw(map_corner, console)
                # Have the actor manager draw the entities so they are consolidated instead of flooding main
                actor_manager.Draw(console, map_corner)

                if eAction != '':
                    console.print(x = 1, y = WorldMap.MAP_VIEW_HEIGHT + 4, string = eAction)
            
                context.present(console)
                refesh_screen = False

            for event in tcod.event.wait():
                context.convert_event(event)
                # print(event) # Debug Log
                action = event_handler.dispatch(event)

                if action is None:
                    continue

                if isinstance(action, MovementAction):                    
                    actor_manager.Move(Vec2(action.dx, action.dy))
                    eAction = ''
                    refesh_screen = True

                elif isinstance(action, ExamineAction):
                    eAction = world.GetExamineAction()
                    refesh_screen = True
                
                elif isinstance(action, EscapeAction):
                    raise SystemExit()

# Main Function

if __name__ == '__main__':
    main()