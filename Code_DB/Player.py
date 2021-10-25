# Player Class, since the player is a unique actor
from Actor import *
from Map import *

class Player(Actor):
    """ Player Class """
    def __init__(self, init_position : Vec2, init_name, init_icon, init_color, map_data : WorldMap):
        super().__init__(init_position, init_name, init_icon, init_color, map_data)
        """ Constructor Specific toward Player """
        self.debug = False
    
    def Move(self, offset : Vec2):
        super().Move(offset)
        if 't' in self.mapLoc:
            if self.map_data.OutsideMap(self.Position()):
                self.position = self.map_data.GetTownLoc()
                self.mapLoc = 'o:'
                self.map_data.ChangeMap('o:')

    def Draw(self, console, corner):
        super().Draw(console, corner) # Ensure to conform to the Actor.Draw() first

        # Player Specific functionality
        x = WorldMap.MAP_VIEW_WIDTH + 2
        console.print(x = x, y = 1, string = "Name: " + self.name)

        for s in range(len(self.stats)):
            y = s + 2            
            d = str(self.stats[s])
            console.print(x = x, y = y, string = d)

        # Debug option
        if self.debug:
            console.print(x = 1, y = WorldMap.MAP_VIEW_HEIGHT + 2, string = str(self.position))