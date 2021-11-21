# Actor functions, used as a base class for
# The player, Monsters and NPCs (once implemented)

from MathFun import *
import Map
from Stats import *
import random
import ColorPallet

class Actor:
    """ Actor class for game entities """

    def __init__(self, init_name, init_icon, init_color, map_data, ai_manager):
        """ Constructor """
        # Initial, default values
        self.position = Vec2(0, 0) # default location
        self.mapLoc = 'o:'
        self.stats = {}
        self.FSM = None # this will be assigned case by case, but in parent class to ensure intellisense
        self.actorType = 'Generic'
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
        for stats in self.stats.keys():
            sd += '<STAT>,'
            sd += stats + ','
            sd += self.stats[stats].sName + ','
            sd += str(self.stats[stats].base_val) + ','
            sd += str(self.stats[stats].mod_val) + ','
            sd += str(self.stats[stats].stat_type) + ','
            sd += ';'
        return sd

    def CreateStats(self):
        """ 
            Creates the stat list for this entity
        """        
        self.stats['Hit Points'] = Stat('HP', 5, 5, 1, 'Vit', 2)
        self.stats['Strength'] = Stat('Str', 5, 0, 0)
        self.stats['Dexterity'] = Stat('Dex', 5, 0, 0)
        self.stats['Vitality'] = Stat('Vit', 5, 0, 0)
        self.stats['Damage'] = Stat('Dmg', 1, 0, 0, 'Str', 2)

    def IsDead(self):
        """ Checks if this actor's hp is empty and returns true or false """
        return self.stats['Hit Points'].mod_val <= 0
    
    def LoadStats(self, new_stats : dict):
        """ Used for loading a game, this takes a dictionary of stats and replaces the current stats """
        self.stats = new_stats

    def Update(self, offset : Vec2):
        """ Update for game loop purposes """
        self.Move(offset)
    
    def OnCollide(self, other):
        """ Determine what to do on colliding """
        self.SendMessage(self.name + ' says hello to ' + other.name + '.')

    def Move(self, offset : Vec2):
        """ Moves an actor """
        # Check if someone else is occupying this space
        collide = self.parent.CheckCollision(self, offset)

        # If nothing was collided, then we can skip this
        if collide != None:
            self.OnCollide(collide)
            return False # couldn't move

        # Check if a space is blocked or not. If it is, we cannot move here
        if not self.map_data.SpaceBlocked(self.position + offset, False) and collide == None:
            self.position += offset
            return True
    
    def Draw(self, display, corner : Vec2):
        """ Displays the character to a screen; Corner = Top Left Corner Map Cord being displayed """
        if corner.x <= self.position.x <= corner.x + Map.WorldMap.MAP_VIEW_WIDTH - 1:
            if corner.y <= self.position.y <= corner.y + Map.WorldMap.MAP_VIEW_HEIGHT - 1:
                # A percent of the actor's health is taken, in order to give a visual "health"
                # ideal. The actor will start at their prescribed color, and slowly interpolate (Lerp)
                # to red upon taking damage.
                p = self.stats['Hit Points'].PercentRemaining() / 100
                col = ColorPallet.ColorLerp(self.color, 'Bloody', p)
                display.print(
                    x = self.position.x - corner.x + 1,
                    y = self.position.y - corner.y + 1,
                    string = self.icon, fg = col)

    def Position(self):
        """ 
            Returns the actors location, but as a copy instead of reference. A copy means we 
            don't accidently change the current value, in the event manipulations are made to
            this value outside of the self.Move(offset) method.
        """
        return self.position.Copy()
    
    def GetMapID(self):
        """ Gets the map this actor is part of """
        return self.mapLoc
    
    def SetSpawn(self, map : str, location : Vec2):
        """ Set's the actor's map location, 'code: cordinates', and their location within the map (x, y)."""
        self.mapLoc = map
        self.position = location

    # Helper functions
    def CanSeeTarget(self, target : Vec2):
        """ Can I see the target (per their location) """
        if self.position.Distance(target) > self.sight:
            return False
        raycast = self.Position() # Create a copy for manipulation
        # Linearly move toward target, able to move diagonally. If the view is blocked, then we can't see
        # The name Raycast is taken from unity, as in casting a ray from point A to B, and returning what
        # found between the two points. In this case, it tests if the terrain blocks sight, and if so,
        # we cannot see the target. Unless the target is the terrain we are searching for.
        while raycast != target:
            if raycast.x < target.x:
                raycast.x += 1
            elif raycast.x > target.x:
                raycast.x -= 1
            if raycast.y < target.y:
                raycast.y += 1
            elif raycast.y > target.y:
                raycast.y -= 1
            if self.map_data.GetTerrainFeature(raycast)[Map.SYMBOL_BLOCK_VIEW]:
                return False
        return True

    # Combat Functions
    def Attack(self, defender):
        """ Attack the defender """
        dmg = self.stats['Damage'].Total()
        hit = random.random() < 0.75
        if hit:
            self.SendMessage(self.name + ' hits ' + defender.name + ' for ' + str(dmg) + ' damage!')
            defender.TakeHit(dmg)
        else:
            self.SendMessage(self.name + ' misses ' + defender.name + '.')
        if defender.IsDead():
            self.parent.Defeated(self, defender)


    def TakeHit(self, damage):
        """ Receive damage. 'Negative' damage can be used to heal, but will make a heal function instead. """
        self.stats['Hit Points'].AddTo(-damage)        
