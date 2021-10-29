# Map Class, for making and using the map
# of the "world"

import tcod
import random
import ColorPallet
import MathFun
from Noise import *
from NameGen import *
from TownGen import TownGenerator
from DungeonGen import DungeonGenerator

# For maps only, or map manipulation (such as A* and entity placement)
# Dictionary : Key => Terrain Feature
# List:
# 0 => Symbol
# 1 => Color (from color pallet. Colors do not exist will print a warning to the console and default to [255, 0, 255])
# 2 => Does this feature block normal movement
# 3 => Description when "examined"
MAP_SYMBOLS = { 
        # Acts as the "barrier" of sorts
        'Water' : ['~', "Blue", True, "You see water, so beautiful and blue. You can get lost for hours just watching the waves hit the shore."],
        # Natural Tiles
        'Dirt' : ['.', "Brown", False, "You see plain soil, perfect for planting things or starting a home."],
        'Grass' : ['v', "Green", False, "You see a field of grass with some flowers sprinkled in."],
        'Sand' : [chr(0x2248), "Tan", False, "You see sand for miles, only golden, hot sand."],
        'Mountains' : ['M', "Olive", True, "You see majestic mountains, much higher than you want to climb."],
        'Room Floor' : ['.', "Light Grey", False, "You see a nice flooring for a room."],
        # Blocking Tiles
        'Wall' : ['#', "Grey", True, "You see a wall. It stands to block you progression."],
        'Road' : [chr(0xB1), "Dark Grey", False, "You see a road, improved to show travelers where to go."],
        # Tiles with special actions, like flowers or portals
        'Town' : ['A', "Tristian", False, "You see a town."],
        'Door' : ['D', "Olive", False, "You see a door, the mortal foe to many would-be adventurers."],
        'Portal' : ['0', "Portal", False, "You see a portal. Who knows what perils await?"],
        'Void' : [' ', 'Black', True, "You see nothing here."],
        'Upstairs' : [chr(0x2264), 'Portal', False, "You see stairs going up"],
        'Downstairs' : [chr(0x2265), 'Portal', False, "You see stairs going down"]
    }

# Indexes for specific map functions, ie: towns and dungeon headers
HEADER = 0
MAP_NAME = 0
MAP_WIDTH = 1
MAP_HEIGHT = 2
DUNGEON_LEVEL = 3
UPSTAIRS = 4
DOWNSTAIRS = 5
MAP_ASTAR = 6

class WorldMap:
    """ Map Class, used to store map data """
    # Symbols = [Name] : Icon, Color, Block Movement
    
    # Drawing parameters for the map, static values that
    # do not need to change unless a new game mode is open
    START_X = 1
    START_Y = 1
    MAP_VIEW_WIDTH = 75
    MAP_VIEW_HEIGHT = 45

    def __init__(self, height, width):
        """ Constructor """
        # Clamp minimum values to avoid complications later
        if height < WorldMap.MAP_VIEW_HEIGHT:
            height = WorldMap.MAP_VIEW_HEIGHT
        if width < WorldMap.MAP_VIEW_WIDTH:
            width = WorldMap.MAP_VIEW_WIDTH

        self.height = height # Overword Height
        self.width = width # Overworld Width
        self.curMapType = 'o' # Defaults the start point to the overworld
        self.player = None # Does not build the player to start with
        self.mapName = GenTownName() # For now, the world gets a random name. Will fix later
        self.mapID = '' # The current "town/dungeon". This is empty for the overworld (as for now, there is only one)
        self.overworld = [] # The overworld map - May make endless later
        self.towns = {} # A dictionary containing data for every town
        self.dungeons = {} # A dictionary containing data for every dungeon
        self.noise = Noise(256) # Initialize the noise engine

    # Generation Techniques for the world, towns and dungeons

    def BuildOverworld(self):
        """ Builds an overworld map """
        # Builds the baseline for terrain. May layer noise later for more interesting looking maps.
        noise_map = self.noise.BuildMap(self.width, self.height, Vec2(0, 0), 23.14)
        # This assumes we are building a new world, and will override the old one if it exists
        self.overworld = []

        for row in range(self.height):
            new_row = []
            for col in range(self.width):
                symbol = 'Grass' # Default tile, for now
                # The noise function returns a range from -1 to 1, unclamped
                # This means that we may get a rare value that is < -1 or > 1.
                if noise_map[row][col] <= -0.11: 
                    symbol = 'Water'
                elif noise_map[row][col] <= -0.05:
                    symbol = 'Sand'
                elif 0.3 <= noise_map[row][col]:
                    symbol = 'Mountains'
                else:
                    map_decor = random.random()
                    if  map_decor < 0.005:
                        symbol = 'Portal'
                    elif map_decor < 0.01:
                        symbol = 'Town'
                new_row += [symbol]
            self.overworld += [new_row]

    def BuildTown(self, t_name, t_cord):
        """ Builds a town """
        # Town: Dict Key => Coord : str(Vec2)
        # 0: Map Data
        # 1+: Tile Data
        tRNG = random.Random(t_name)
        town_width = tRNG.randrange(WorldMap.MAP_VIEW_WIDTH,WorldMap.MAP_VIEW_WIDTH * 2)
        town_height = tRNG.randrange(WorldMap.MAP_VIEW_HEIGHT, WorldMap.MAP_VIEW_HEIGHT * 2)
        
        # Build the map using an external function, as to not bloat the map drawing class
        new_map = TownGenerator(town_height, town_width)
        # If we are making the town, then the town 
        # does not exist in the dictionary yet.
        self.towns[t_cord] = [[t_name, town_width, town_height]] # Header for all towns/dungeons
        # Add the town to the dictionary of maps
        for y in range(town_height):
            self.towns[t_cord] += [new_map[y]]

    def BuildDungeon(self, d_name, d_cord):
        """ Builds a dungeon """
        # Town: Dict Key => Coord : str(Vec2)
        # 0: Map Data
        # 1+: Tile Data
        dungeon_level = int(d_cord.split(',')[2])
        dRNG = random.Random(d_name)
        dungeon_width = dRNG.randrange(WorldMap.MAP_VIEW_WIDTH,WorldMap.MAP_VIEW_WIDTH * 2)
        dungeon_height = dRNG.randrange(WorldMap.MAP_VIEW_HEIGHT, WorldMap.MAP_VIEW_HEIGHT * 2)

        self.dungeons[d_cord] = DungeonGenerator([d_name, dungeon_width, dungeon_height, dungeon_level], dRNG)        

    # Helper functions for manipulating map functions and such

    def SetPlayer(self, player):
        """ Sets the player character for map operations """
        self.player = player

    def GetTerrainFeature(self, loc : Vec2, getIndex = False):
        """ 
            Gets the Map Symbol (returns the whole list) for a spot,
            Highly dependant of the currently displayed map.
        """
        sym = MAP_SYMBOLS["Void"] # The default
        if self.curMapType == 'o':
            index = self.overworld[loc.y][loc.x]
            if getIndex:
                return index
            sym = MAP_SYMBOLS[index]
        elif self.curMapType == 't':
            index = self.towns[self.mapID][loc.y + 1][loc.x]
            if getIndex:
                return index
            sym = MAP_SYMBOLS[index]
        elif self.curMapType == 'd':
            index = self.dungeons[self.mapID][loc.y + 1][loc.x]
            if getIndex:
                return index
            sym = MAP_SYMBOLS[index]
        return sym

    # Need to change that this only examines, and not uses, the terrain feature
    def GetExamineAction(self):
        """ Determines the action to take when at a location when examine/use is pressed """
        feature = self.GetTerrainFeature(self.player.Position(), True)
        sym = MAP_SYMBOLS[feature]

        s = sym[3]

        if feature == "Town":
            t_loc = str(self.player.position.x) + ',' + str(self.player.position.y)
            if t_loc not in self.towns:
                self.BuildTown(GenTownName(), t_loc)
            s += '\nWelcome to ' + self.towns[t_loc][HEADER][MAP_NAME] + '.'
            self.ChangeMap('t:' + t_loc)
            self.player.mapLoc = 't:' + t_loc
            self.player.position = Vec2(self.towns[t_loc][HEADER][MAP_WIDTH]//2, self.towns[t_loc][HEADER][MAP_HEIGHT] - 1)
        if feature == "Portal":
            d_loc = str(self.player.position.x) + ',' + str(self.player.position.y) + ',1'
            if d_loc not in self.dungeons:
                self.BuildDungeon(GenTownName(), d_loc)
            s += '\nYou have entered ' + self.dungeons[d_loc][HEADER][MAP_NAME] + '.'
            self.ChangeMap('d:' + d_loc)
            self.player.mapLoc = 'd:' + d_loc
            self.player.position = Vec2(self.dungeons[d_loc][HEADER][UPSTAIRS].x, self.dungeons[d_loc][HEADER][UPSTAIRS].y)
        if feature == "Upstairs":
            m = self.mapID.split(',')
            lvl = int(m[2]) # Get the current level
            if lvl <= 1:
                s += '\nYou Have escaped the dungeon, ' + self.dungeons[self.mapID][HEADER][MAP_NAME] + '.'
                self.ChangeMap('o:')
                self.player.mapLoc = 'o:'
                self.player.position = Vec2(int(m[0]), int(m[1]))
            else:
                s += '\nYou have traveled up a level in the dungeon.'
                new_map = m[0] + ',' + m[1] + ',' + str(lvl - 1)
                # In the event this dungeon portion does not exist for some reason
                if new_map not in self.dungeons:
                    d_name = self.dungeons[m[0] + ',' + m[1] + ',1'][HEADER][MAP_NAME]
                    self.BuildDungeon(d_name, new_map)
                self.ChangeMap('d:' + new_map)
                self.player.position = Vec2(self.dungeons[new_map][HEADER][DOWNSTAIRS].x, self.dungeons[new_map][HEADER][DOWNSTAIRS].y)
                self.player.mapLoc = 'd:' + new_map
        if feature == "Downstairs":
            m = self.mapID.split(',')
            lvl = int(m[2])
            s += '\nYou have traveled down a level in the dungeon.'
            new_map = m[0] + ',' + m[1] + ',' + str(lvl + 1)
            if new_map not in self.dungeons:
                d_name = self.dungeons[m[0] + ',' + m[1] + ',1'][HEADER][MAP_NAME]
                self.BuildDungeon(d_name, new_map)
            self.ChangeMap('d:' + new_map)
            self.player.position = Vec2(self.dungeons[new_map][HEADER][UPSTAIRS].x, self.dungeons[new_map][HEADER][UPSTAIRS].y)
            self.player.mapLoc = 'd:' + new_map

        return s

    def ChangeMap(self, new_map : str):
        """ Changes the map based on the string """
        m = new_map.split(':')
        self.curMapType = m[0]
        if m[0] == 'o':
            self.mapID = ''
        else:
            self.mapID = m[1]

    def OutsideMap(self, loc : Vec2):
        """ Checks if a point is outside the bounds of the current map """
        width = self.width
        height = self.height
        if self.curMapType == 't':
            width = self.towns[self.mapID][HEADER][MAP_WIDTH]
            height = self.towns[self.mapID][HEADER][MAP_HEIGHT]
        return loc.x < 0 or loc.y < 0 or loc.x >= width or loc.y >= height
    
    def GetTownLoc(self):
        """ Gets the location of the current town. Not valid if this location is not in a town """
        m = self.mapID.split(',')
        return Vec2(int(m[0]), int(m[1]))
    
    def GetDungeonLoc(self):
        """ Gets the location of the current dungeon. """
        m = self.mapID.split(',')
        return Vec2(int(m[0]), int(m[1]))
    
    def GetEmptySpot(self, mapLoc : str):
        """ Finds a random empty spot on the map """
        m = mapLoc.split(':')
        while True: # DANGEROUS INFINITE LOOP POTENTIAL !!!!
            if m[0] == 'o':
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                if not MAP_SYMBOLS[self.overworld[y][x]][2]:
                    return Vec2(x, y)
            elif m[0] == 't':
                return Vec2(0, 0) # Generic for now
            elif m[0] == 'd':
                return Vec2(0, 0) # Generic for now

    def SpaceBlocked(self, cord : MathFun.Vec2):
        """ 
            Checks if a location is blocked
            Map Index:
            o: Overworld
            t: Vector2 - Towns
            d: x, y, level - Dungeons
        """
        if self.curMapType == 'o':
            # To prevent out of array issues, assume the map edges are blocked
            if cord.x < 0 or cord.x >= self.width:
                return True
            if cord.y < 0 or cord.y >= self.height:
                return True
            return MAP_SYMBOLS[self.overworld[cord.y][cord.x]][2] # <--- That is almost a nightmare to remember!
        elif self.curMapType == 't':
            if cord.x < 0 or cord.x >= self.towns[self.mapID][HEADER][MAP_WIDTH]:
                return False
            if cord.y < 0 or cord.y >= self.towns[self.mapID][HEADER][MAP_HEIGHT]:
                return False
            return MAP_SYMBOLS[self.towns[self.mapID][cord.y+1][cord.x]][2]
        elif self.curMapType == 'd':
            if cord.x < 0 or cord.x >= self.dungeons[self.mapID][HEADER][MAP_WIDTH]:
                return True
            if cord.y < 0 or cord.y >= self.dungeons[self.mapID][HEADER][MAP_HEIGHT]:
                return True
            return MAP_SYMBOLS[self.dungeons[self.mapID][cord.y+1][cord.x]][2]

    # Functions to draw the maps

    def Draw(self, start : MathFun.Vec2, display : tcod.Console):
        """ 
            Draws a map
            Map Index:
            o: - Overworld
            t: <Name> - Towns
            d: x, y, level - Dungeons
        """
        map_display_loc = Vec2(WorldMap.MAP_VIEW_WIDTH - 2, WorldMap.MAP_VIEW_HEIGHT + 2)
        if self.curMapType == 'o':
            display.print(x = map_display_loc.x, y = map_display_loc.y, string = 'Overworld')
            self.DrawOverworld(start, display)
        if self.curMapType == 't':
            town_name = 'Town: ' + self.towns[self.mapID][HEADER][MAP_NAME]
            display.print(x = map_display_loc.x, y = map_display_loc.y, string = town_name)
            self.DrawTown(start, display)
        if self.curMapType == 'd':
            m = self.mapID.split(',')
            dungeon_name = 'Dungeon: ' + self.dungeons[self.mapID][HEADER][MAP_NAME] + " L: " + m[2]
            display.print(x = map_display_loc.x, y = map_display_loc.y, string = dungeon_name)
            self.DrawDungeon(start, display)

    def DrawTown(self, start : MathFun.Vec2, display : tcod.Console):
        """ Draws a town """
        # Simplify the use of the repetitive data
        width = self.towns[self.mapID][HEADER][MAP_WIDTH]
        height = self.towns[self.mapID][HEADER][MAP_HEIGHT]
        
        start.x = Clamp(0, width - WorldMap.MAP_VIEW_WIDTH, start.x)
        start.y = Clamp(0, height - WorldMap.MAP_VIEW_HEIGHT, start.y)

        for x in range(WorldMap.MAP_VIEW_WIDTH):
            for y in range(WorldMap.MAP_VIEW_HEIGHT):
                # Get the index
                index = self.towns[self.mapID][start.y + y + 1][start.x + x]
                icon = MAP_SYMBOLS[index][0]
                color = ColorPallet.GetColor(MAP_SYMBOLS[index][1])
                display.print(x = x + WorldMap.START_X, 
                    y = y + WorldMap.START_Y, string = icon, fg = color)
        

    def DrawDungeon(self, start : MathFun.Vec2, display : tcod.Console):
        """ Draws the dungeon at a x/y/z coord """
        # Simplify the use of the repetitive data
        width = self.dungeons[self.mapID][HEADER][MAP_WIDTH]
        height = self.dungeons[self.mapID][HEADER][MAP_HEIGHT]
        
        # Clamp the values of x and y
        start.x = Clamp(0, width - WorldMap.MAP_VIEW_WIDTH, start.x)
        start.y = Clamp(0, height - WorldMap.MAP_VIEW_HEIGHT, start.y)

        for x in range(WorldMap.MAP_VIEW_WIDTH):
            for y in range(WorldMap.MAP_VIEW_HEIGHT):
                # Get the index
                index = self.dungeons[self.mapID][start.y + y + 1][start.x + x]
                icon = MAP_SYMBOLS[index][0]
                color = ColorPallet.GetColor(MAP_SYMBOLS[index][1])
                display.print(x = x + WorldMap.START_X, 
                    y = y + WorldMap.START_Y, string = icon, fg = color)

    def DrawOverworld(self, start : MathFun.Vec2, display : tcod.Console):
        """ Draw Overworld (main map) to the screen """
        start.x = Clamp(0, self.width - WorldMap.MAP_VIEW_WIDTH, start.x)
        start.y = Clamp(0, self.height - WorldMap.MAP_VIEW_HEIGHT, start.y)

        for x in range(WorldMap.MAP_VIEW_WIDTH):
            for y in range(WorldMap.MAP_VIEW_HEIGHT):
                # Get the index
                index = self.overworld[start.y + y][start.x + x]
                icon = MAP_SYMBOLS[index][0]
                color = ColorPallet.GetColor(MAP_SYMBOLS[index][1])
                display.print(x = x + WorldMap.START_X, 
                    y = y + WorldMap.START_Y, string = icon, fg = color)