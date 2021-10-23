# Actor functions

#tcod for actor placement
from MathFun import *
from Map import *
from Stats import *

class Actor:
    """ Actor class for game entities """

    def __init__(self, init_position : Vec2, init_name, init_icon, init_color, map_data : WorldMap):
        """ Constructor """
        self.position = init_position
        self.name = init_name
        self.icon = init_icon
        self.mapLoc = 'o:'
        self.color = init_color
        self.sight = 5
        self.map_data = map_data
        # Creates a spawn point for the entity
        self.CreateSpawn()

        self.stats = [
            Stat('Hit Points', 'HP', 5, 5, 1),
            Stat('Mana', 'MP', 5, 5, 1),
            Stat('Strength', 'Str', 5, 0, 0),
            Stat('Dexterity', 'Dex', 5, 0, 0),
            Stat('Vitality', 'Vit', 5, 0, 0)
            ]

    def CreateSpawn(self):
        """ Creates a spawn point and ensures it isn't in a blocked location """
        self.position = self.map_data.GetEmptySpot(self.mapLoc)

    def Move(self, offset : Vec2):
        """ Moves an actor """
        # Check if a space is blocked or not. If it is, we cannot move here
        if not self.map_data.SpaceBlocked(self.position + offset):
            self.position += offset
    
    def Draw(self, display, corner : Vec2):
        """ Displays the character to a screen; Corner = Top Left Corner Map Cord being displayed """
        if not self.mapLoc == self.map_data.curMapType + ':' + self.map_data.mapID:
            return # Do not do anything if we are on the wrong map to draw this character

        if corner.x <= self.position.x <= corner.x + WorldMap.MAP_VIEW_WIDTH:
            if corner.y <= self.position.y <= corner.y + WorldMap.MAP_VIEW_HEIGHT:
                display.print(
                    x = self.position.x - corner.x + 1, 
                    y = self.position.y - corner.y + 1, 
                    string = self.icon, fg = self.color)

    def Position(self):
        """ Returns the actors location """
        return Vec2(self.position.x, self.position.y)