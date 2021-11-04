# Actor functions

#tcod for actor placement
from MathFun import *
import Map
from Stats import *
import ColorPallet

class Actor:
    """ Actor class for game entities """

    def __init__(self, init_name, init_icon, init_color, map_data, ai_manager):
        """ Constructor """
        # Initial, default values
        self.position = Vec2(0, 0) # default location
        self.mapLoc = 'o:'
        self.stats = []
        self.FSM = None # this will be assigned case by case, but in parent class to ensure intellisense
        # Added by class
        self.name = init_name
        self.icon = init_icon        
        self.color = init_color
        self.parent = ai_manager
        # Base Stats
        self.sight = 5
        self.map_data = map_data # reference only
        self.CreateStats()

    def SendMessage(self, message : str):
        """ Send a message to the log system """
        self.parent.AddLog(message)

    def SaveFormatter(self):
        """ Builds a string specifically for saving data """
        sd = ''
        sd += self.name + ';' # Name
        sd += self.mapLoc + ';' # Map ID
        sd += str(self.position) + ';' # Position on map
        for stats in self.stats:
            sd += '<stat>,'
            sd += stats.sName + ','
            sd += stats.lName + ','
            sd += str(stats.base_val) + ','
            sd += str(stats.mod_val) + ','
            sd += str(stats.stat_type) + ','
            sd += ';'
        return sd

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

    def Update(self, offset : Vec2):
        """ Update for game loop purposes """
        self.Move(offset)
    
    def Move(self, offset : Vec2):
        """ Moves an actor """
        # Check if a space is blocked or not. If it is, we cannot move here
        if not self.map_data.SpaceBlocked(self.position + offset):
            self.position += offset
    
    def Draw(self, display, corner : Vec2):
        """ Displays the character to a screen; Corner = Top Left Corner Map Cord being displayed """
        if corner.x <= self.position.x <= corner.x + Map.WorldMap.MAP_VIEW_WIDTH:
            if corner.y <= self.position.y <= corner.y + Map.WorldMap.MAP_VIEW_HEIGHT:
                display.print(
                    x = self.position.x - corner.x + 1,
                    y = self.position.y - corner.y + 1,
                    string = self.icon, fg = ColorPallet.GetColor(self.color))

    def Position(self):
        """ Returns the actors location, but as a copy instead of reference """
        return self.position.Copy()
    
    def GetMapID(self):
        """ Gets the map this actor is part of """
        return self.mapLoc
    
    def SetSpawn(self, map : str, location : Vec2):
        self.mapLoc = map
        self.position = location

    # Helper functions
    def CanSeeTarget(self, target : Vec2):
        """ Can I see the target (per their location) """
        if self.position.Distance(target) > self.sight:
            return False
        raycast = self.Position() # Create a copy for manipulation
        # Linearly move toward target, able to move diagonally. If the view is blocked, then we can't see
        while raycast != target:
            if raycast.x < target.x:
                raycast.x += 1
            if raycast.x > target.x:
                raycast.x -= 1
            if raycast.y < target.y:
                raycast.y += 1
            if raycast.y > target.y:
                raycast.y -= 1
            if self.map_data.GetTerrainFeature(raycast)[Map.SYMBOL_BLOCK_VIEW]:
                return False
        return True