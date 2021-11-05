# Player Class, since the player is a unique actor
from Actor import *
from Map import *
from Monster import Monster

class Player(Actor):
    """ Player Class """
    def __init__(self, map_data : WorldMap, ai_manager):
        super().__init__("Default", '@', 'White', map_data, ai_manager)
        """ Constructor Specific toward Player """
        
        self.actorType = 'Player'
        self.debug = False
    
    def Update(self, offset : Vec2):
        self.Move(offset)
        if 't' in self.mapLoc:
            if self.map_data.OutsideMap(self.Position()):
                self.position = self.map_data.GetTownLoc()
                self.mapLoc = 'o:'
                self.map_data.ChangeMap('o:')

    def OnCollide(self, other):
        """ What happens when the actor collides with something """
        if other.actorType == 'Monster':
            self.Attack(other)
        else:
            return super().OnCollide(other)

    def Draw(self, console, corner):
        super().Draw(console, corner) # Ensure to conform to the Actor.Draw() first

        # Player Specific functionality
        x = WorldMap.MAP_VIEW_WIDTH + 2
        console.print(x = x, y = 1, string = "Name: " + self.name)
        y = 2
        for stat in self.stats.keys():
            d = str(self.stats[stat])
            console.print(x = x, y = y, string = d)
            y += 1

        console.print(x = WorldMap.MAP_VIEW_WIDTH - 2, y = WorldMap.MAP_VIEW_HEIGHT + 3, string = str(self.position.ToString()))