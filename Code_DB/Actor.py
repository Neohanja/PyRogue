# Actor functions

#tcod for actor placement
from MathFun import *
from Map import *
from Stats import *
import ColorPallet

class Actor:
    """ Actor class for game entities """

    def __init__(self, init_name, init_icon, init_color, map_data : WorldMap):
        """ Constructor """
        # Initial, default values
        self.position = Vec2(0, 0) # default location
        self.mapLoc = 'o:'
        self.stats = []
        # Added by class
        self.name = init_name
        self.icon = init_icon        
        self.color = init_color
        # Base Stats
        self.sight = 5
        self.map_data = map_data # reference only        

    def CreateStats(self):
        """ 
            Creates the stat list for this entity; 
            Super() should always be included for child classes 
        """        
        self.stats.append(Stat('Hit Points', 'HP', 5, 5, 1))
        self.stats.append(Stat('Mana', 'MP', 5, 5, 1))
        self.stats.append(Stat('Strength', 'Str', 5, 0, 0))
        self.stats.append(Stat('Dexterity', 'Dex', 5, 0, 0))
        self.stats.append(Stat('Vitality', 'Vit', 5, 0, 0))

    def Move(self, offset : Vec2):
        """ Moves an actor """
        # Check if a space is blocked or not. If it is, we cannot move here
        if not self.map_data.SpaceBlocked(self.position + offset):
            self.position += offset
    
    def Draw(self, display, corner : Vec2):
        """ Displays the character to a screen; Corner = Top Left Corner Map Cord being displayed """
        if corner.x <= self.position.x <= corner.x + WorldMap.MAP_VIEW_WIDTH:
            if corner.y <= self.position.y <= corner.y + WorldMap.MAP_VIEW_HEIGHT:
                display.print(
                    x = self.position.x - corner.x + 1,
                    y = self.position.y - corner.y + 1,
                    string = self.icon, fg = ColorPallet.GetColor(self.color))

    def Position(self):
        """ Returns the actors location """
        return Vec2(self.position.x, self.position.y)
    
    def GetMapID(self):
        """ Gets the map this actor is part of """
        return self.mapLoc
    
    def SetSpawn(self, map : str, location : Vec2):
        self.mapLoc = map
        self.position = location
