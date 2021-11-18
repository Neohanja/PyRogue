# Map Class, for making and using the map
# of the "world"

import tcod
import random
from AStar import AStar
import ColorPallet
import MathFun
from Noise import *
from NameGen import *
from TownGen import *
from DungeonGen import DungeonGenerator

# For maps only, or map manipulation (such as A* and entity placement)
# Dictionary : Key => Terrain Feature
# List:
SYMBOL_ICON = 0
SYMBOL_COLOR = 1
SYMBOL_BLOCK_MOVEMENT = 2
SYMBOL_BLOCK_VIEW = 3
SYMBOL_GEN_DESCRIPTION = 4
# 0 => Symbol
# 1 => Color (from color pallet. Colors do not exist will print a warning to the console and default to [255, 0, 255])
# 2 => Does this feature block normal movement
# 3 => Description when "examined"
MAP_SYMBOLS = { 
        # Acts as the "barrier" of sorts
        'Water' : ['~', "Blue", True, False, 
            "You see water, so beautiful and blue. You can get lost for hours just watching the waves hit the shore."],
        # Natural Tiles
        'Dirt' : ['.', "Brown", False, False,
            "You see plain soil, perfect for planting things or starting a home."],
        'Grass' : ['v', "Green", False, False,
            "You see a field of grass with some flowers sprinkled in."],
        'Sand' : [chr(0x2248), "Tan", False, False,
            "You see sand for miles, only golden, hot sand."],
        'Mountains' : ['M', "Olive", True, True,
            "You see majestic mountains, much higher than you want to climb."],
        'Room Floor' : ['.', "Light Grey", False, False,
            "You see a nice flooring for a room."],
        # Blocking Tiles
        'Wall' : ['#', "Grey", True, True,
            "You see a wall. It stands to block you progression."],
        'Road' : [chr(0xB1), "Dark Grey", False, False,
            "You see a road, improved to show travelers where to go."],
        # Tiles with special actions, like flowers or portals
        'Town' : ['A', "Tristian", False, False,
            "You see a town."],
        'Door' : ['D', "Olive", False, False,
            "You see a door, the mortal foe to many would-be adventurers."],
        'Portal' : ['0', "Portal", False, False,
            "You see a portal. Who knows what perils await?"],
        'Void' : [' ', 'Black', True, False,
            "You see nothing here."],
        'Upstairs' : [chr(0x2264), 'Portal', False, False,
            "You see stairs going up"],
        'Downstairs' : [chr(0x2265), 'Portal', False, False,
            "You see stairs going down"]
    }

# Indexes for specific map functions, ie: towns and dungeon headers
HEADER = 0
MAP_NAME = 0
MAP_WIDTH = 1
MAP_HEIGHT = 2
MAP_RNG = 3
# Dungeon Specific
DUNGEON_LEVEL = 4
UPSTAIRS = 5
DOWNSTAIRS = 6
# Town Specific (Once needed/Used)
TOWN_NPCS = 4
TOWN_QUESTS = 5
# Town somthing = 6
# Overworld Specific (Once needed/Used)
WORLD_SEED = 4
OVER_TOWNS = 5
OVER_DUNGEONS = 6
# A* Pathfinding Module
MAP_ASTAR = 7

class WorldMap:
    """ Map Class, used to store map data """
    
    # Drawing parameters for the map, static values that
    # do not need to change unless a new game mode is open
    START_X = 1
    START_Y = 1
    MAP_VIEW_WIDTH = 75
    MAP_VIEW_HEIGHT = 45

    def __init__(self, height, width, seedName = 'Drakland'):
        """ Constructor """
        # Clamp minimum values to avoid complications later
        if height < WorldMap.MAP_VIEW_HEIGHT:
            height = WorldMap.MAP_VIEW_HEIGHT
        if width < WorldMap.MAP_VIEW_WIDTH:
            width = WorldMap.MAP_VIEW_WIDTH

        # Generate the world header
        # Temporary: World seed is 'Drakland'. Should be a string to ensure continuity with all "seeds"
        overworld_header = [seedName, width, height, random.Random(seedName), seedName, {}, {}]
        self.worldSeed = ''
        self.curMapType = 'o' # Defaults the start point to the overworld
        self.player = None # Does not build the player to start with
        self.mapID = '' # The current "town/dungeon". This is empty for the overworld (as for now, there is only one)
        self.overworld = [] # The overworld map - May make endless later
        self.towns = {} # A dictionary containing data for every town
        self.dungeons = {} # A dictionary containing data for every dungeon
        self.noise = None # Reserve the name
        self.BuildOverworld(overworld_header)

    # Generation Techniques for the world, towns and dungeons
    def BuildOverworld(self, overworld_header : list):
        """ Builds an overworld map """
        # Get the important values from the header
        height = overworld_header[MAP_HEIGHT]
        width = overworld_header[MAP_WIDTH]
        wRNG = overworld_header[MAP_RNG]
        self.noise = Noise(256, wRNG)
        
        # Builds the baseline for terrain. May layer noise later for more interesting looking maps.
        noise_map = self.noise.BuildMap(width, height, Vec2(0, 0), 23.14)
        # This assumes we are building a new world, and will override the old one if it exists
        self.overworld = [overworld_header]
        self.worldSeed = overworld_header[MAP_NAME]
        
        for row in range(height):
            new_row = []
            for col in range(width):
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
                    map_decor = wRNG.random()
                    terrainID = str(col) + ',' + str(row)
                    if  map_decor < 0.005:
                        symbol = 'Portal'
                        overworld_header[OVER_DUNGEONS][terrainID] = GenTownName(self.worldSeed + terrainID)
                new_row += [symbol]
            self.overworld += [new_row]

        overworld_header.append(AStar(self.overworld[1:]))
        PlaceTowns(self.overworld)

    def BuildTown(self, t_cord):
        """ Builds a town """
        tRNG = random.Random(self.worldSeed + t_cord)
        town_width = tRNG.randrange(WorldMap.MAP_VIEW_WIDTH,WorldMap.MAP_VIEW_WIDTH * 2)
        town_height = tRNG.randrange(WorldMap.MAP_VIEW_HEIGHT, WorldMap.MAP_VIEW_HEIGHT * 2)
        
        town_header = [self.overworld[HEADER][OVER_TOWNS][t_cord], town_width, town_height, tRNG]

        # Build the map using an external function, as to not bloat the map drawing class
        new_map = TownGenerator(town_header)
        # If we are making the town, then the town 
        # does not exist in the dictionary yet.
        self.towns[t_cord] = [town_header] # Header for all towns/dungeons
        # Add the town to the dictionary of maps
        for y in range(town_height):
            self.towns[t_cord] += [new_map[y]]

    def BuildDungeon(self, d_cord):
        """ Builds a dungeon """
        d = d_cord.split(',')
        dungeon_level = int(d[2])
        d_index = d[0] + ',' + d[1]
        dRNG = random.Random(self.worldSeed + d_cord)
        dungeon_width = dRNG.randrange(WorldMap.MAP_VIEW_WIDTH,WorldMap.MAP_VIEW_WIDTH * 2)
        dungeon_height = dRNG.randrange(WorldMap.MAP_VIEW_HEIGHT, WorldMap.MAP_VIEW_HEIGHT * 2)

        self.dungeons[d_cord] = DungeonGenerator([self.overworld[HEADER][OVER_DUNGEONS][d_index], 
            dungeon_width, dungeon_height, dRNG, dungeon_level])

    # Save and Load Functions
    def SaveMapData(self):
        """ Reads in the map as a full string, then returns it """
        msd = []
        msd += [self.GetMapString('o', '') + '\n']
        for town in self.towns.keys():
            msd += [self.GetMapString('t', town) + '\n']
        for dungeon in self.dungeons.keys():
            msd += [self.GetMapString('d', dungeon) + '\n']
        return msd
        
    def LoadMapData(self, map_lines : list):
        """ Loads in a map """
        self.dungeons.clear()
        self.towns.clear()
        for map_data in map_lines:
            self.CreateMapFromString(map_data)
    
    def CreateMapFromString(self, map_string : str):
        """ Loads a map from a string """
        parsed_map = map_string.split(';')
        mapType = parsed_map[1].split(':')[0]   
        # overworld_header = ['Drakland', height, width, random.Random('Drakland'), 'Drakland', {}, {}]
        if mapType == 'o':
            mapName = parsed_map[2]
            mapdimensions = parsed_map[3].split(',')
            mapWidth = int(mapdimensions[0])
            mapHeight = int(mapdimensions[1])   
            header = [mapName, mapHeight, mapWidth, random.Random(mapName), mapName, {}, {}]
            self.BuildOverworld(header)
            pass
        elif mapType == 'd':
            mapID = parsed_map[1].split(':')[1]  
            self.BuildDungeon(mapID)
            pass
        elif mapType == 't':
            mapID = parsed_map[1].split(':')[1]  
            self.BuildTown(mapID)
            pass

    def GetMapString(self, mapType : str, mapID : str):
        """ Gets the string interpretation of a map """
        st = '<MAP>;' + mapType + ':' + mapID + ';'
        if mapType == 'o':
            height = self.overworld[HEADER][MAP_HEIGHT]
            width = self.overworld[HEADER][MAP_WIDTH]
            st += self.overworld[HEADER][MAP_NAME] + ';'
            st += str(width) + ',' + str(height) + ';'
            return st
        elif mapType == 'd':
            height = self.dungeons[mapID][HEADER][MAP_HEIGHT]
            width = self.dungeons[mapID][HEADER][MAP_WIDTH]
            st += self.dungeons[mapID][HEADER][MAP_NAME] + ','
            st += str(width) + ',' + str(height) + ';'
            return st
        elif mapType == 't':
            height = self.towns[mapID][HEADER][MAP_HEIGHT]
            width = self.towns[mapID][HEADER][MAP_WIDTH]
            st += self.towns[mapID][HEADER][MAP_NAME] + ','
            st += str(width) + ',' + str(height) + ';'
            return st

    # Helper functions for manipulating map functions and such
    def SetPlayer(self, player):
        """ Sets the player character for map operations """
        self.player = player

    def GetPathfinder(self):
        """ Gets the pathfinding engine for the current map """
        if self.curMapType == 'o':
            return self.overworld[HEADER][MAP_ASTAR]
        elif self.curMapType == 't':
            return self.towns[self.mapID][HEADER][MAP_ASTAR]
        elif self.curMapType == 'd':
            return self.dungeons[self.mapID][HEADER][MAP_ASTAR]

    def GetTerrainFeature(self, loc : Vec2, getIndex = False):
        """ 
            Gets the Map Symbol (returns the whole list) for a spot,
            Highly dependant of the currently displayed map.
        """
        sym = MAP_SYMBOLS["Void"] # The default
        if self.curMapType == 'o':
            index = self.overworld[loc.y + 1][loc.x]
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

    def GetExamineAction(self):
        """ Determines the action to take when at a location when examine/use is pressed """
        feature = self.GetTerrainFeature(self.player.Position(), True)
        sym = MAP_SYMBOLS[feature]
        return sym[SYMBOL_GEN_DESCRIPTION]

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
        width = 0
        height = 0
        if self.curMapType == 'o':
            width = self.overworld[HEADER][MAP_WIDTH]
            height = self.overworld[HEADER][MAP_HEIGHT]
        elif self.curMapType == 't':
            width = self.towns[self.mapID][HEADER][MAP_WIDTH]
            height = self.towns[self.mapID][HEADER][MAP_HEIGHT]
        elif self.curMapType == 'd':
            width = self.dungeons[self.mapID][HEADER][MAP_WIDTH]
            height = self.dungeons[self.mapID][HEADER][MAP_HEIGHT]
        return loc.x < 0 or loc.y < 0 or loc.x >= width or loc.y >= height
    
    def GetTownLoc(self):
        """ Gets the location of the current town. Not valid if this location is not in a town """
        if self.curMapType != 't':
            return None
        m = self.mapID.split(',')
        return Vec2(int(m[0]), int(m[1]))

    def GetCurrentMap(self):
        """ Return the Map ID for the currently viewed map """
        return self.curMapType + ':' + self.mapID
    
    def GetDungeonLoc(self):
        """ Gets the location of the current dungeon. """
        m = self.mapID.split(',')
        return Vec2(int(m[0]), int(m[1]))
    
    def GetEmptySpot(self, mapLoc : str):
        """ Finds a random empty spot on the map """
        m = mapLoc.split(':')
        while True: # DANGEROUS INFINITE LOOP POTENTIAL !!!!
            if m[0] == 'o':
                x = random.randint(0, self.overworld[HEADER][MAP_WIDTH] - 1)
                y = random.randint(0, self.overworld[HEADER][MAP_HEIGHT] - 1)
                if not MAP_SYMBOLS[self.overworld[y + 1][x]][SYMBOL_BLOCK_MOVEMENT] and \
                    self.overworld[y + 1][x] != 'Town' and self.overworld[y + 1][x] != 'Portal':
                    return Vec2(x, y)
            elif m[0] == 't':
                width = self.towns[m[1]][HEADER][MAP_WIDTH]
                height = self.towns[m[1]][HEADER][MAP_HEIGHT]
                x = random.randint(0, width - 1)
                y = random.randint(0, height - 1)
                if not MAP_SYMBOLS[self.towns[m[1]][y + 1][x]][SYMBOL_BLOCK_MOVEMENT]:
                    return Vec2(x, y)
            elif m[0] == 'd':
                width = self.dungeons[m[1]][HEADER][MAP_WIDTH]
                height = self.dungeons[m[1]][HEADER][MAP_HEIGHT]
                x = random.randint(0, width - 1)
                y = random.randint(0, height - 1)
                point = Vec2(x, y)
                if not MAP_SYMBOLS[self.dungeons[m[1]][y + 1][x]][SYMBOL_BLOCK_MOVEMENT]:
                    # Make sure this space isn't on top of a stairs
                    if point == self.dungeons[m[1]][HEADER][UPSTAIRS] or point == self.dungeons[m[1]][HEADER][DOWNSTAIRS]:
                        continue
                    return point

    def SpaceBlocked(self, cord : MathFun.Vec2, includeTowns = True):
        """ 
            Checks if a location is blocked
            Map Index:
            o: Overworld
            t: Vector2 - Towns
            d: x, y, level - Dungeons
        """
        if self.curMapType == 'o':
            # To prevent out of array issues, assume the map edges are blocked
            if cord.x < 0 or cord.x >= self.overworld[HEADER][MAP_WIDTH]:
                return True
            if cord.y < 0 or cord.y >= self.overworld[HEADER][MAP_HEIGHT]:
                return True
            if includeTowns and self.overworld[cord.y + 1][cord.x] == 'Town':
                return True
            return MAP_SYMBOLS[self.overworld[cord.y + 1][cord.x]][SYMBOL_BLOCK_MOVEMENT] # <--- That is almost a nightmare to remember!
        elif self.curMapType == 't':
            if cord.x < 0 or cord.x >= self.towns[self.mapID][HEADER][MAP_WIDTH]:
                return False
            if cord.y < 0 or cord.y >= self.towns[self.mapID][HEADER][MAP_HEIGHT]:
                return False
            return MAP_SYMBOLS[self.towns[self.mapID][cord.y+1][cord.x]][SYMBOL_BLOCK_MOVEMENT]
        elif self.curMapType == 'd':
            if cord.x < 0 or cord.x >= self.dungeons[self.mapID][HEADER][MAP_WIDTH]:
                return True
            if cord.y < 0 or cord.y >= self.dungeons[self.mapID][HEADER][MAP_HEIGHT]:
                return True
            return MAP_SYMBOLS[self.dungeons[self.mapID][cord.y+1][cord.x]][SYMBOL_BLOCK_MOVEMENT]

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
                icon = MAP_SYMBOLS[index][SYMBOL_ICON]
                color = ColorPallet.GetColor(MAP_SYMBOLS[index][SYMBOL_COLOR])
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
                icon = MAP_SYMBOLS[index][SYMBOL_ICON]
                color = ColorPallet.GetColor(MAP_SYMBOLS[index][SYMBOL_COLOR])
                display.print(x = x + WorldMap.START_X, 
                    y = y + WorldMap.START_Y, string = icon, fg = color)

    def DrawOverworld(self, start : MathFun.Vec2, display : tcod.Console):
        """ Draw Overworld (main map) to the screen """
        start.x = Clamp(0, self.overworld[HEADER][MAP_WIDTH] - WorldMap.MAP_VIEW_WIDTH, start.x)
        start.y = Clamp(0, self.overworld[HEADER][MAP_HEIGHT] - WorldMap.MAP_VIEW_HEIGHT, start.y)

        for x in range(WorldMap.MAP_VIEW_WIDTH):
            for y in range(WorldMap.MAP_VIEW_HEIGHT):
                # Get the index
                index = self.overworld[start.y + y + 1][start.x + x]
                icon = MAP_SYMBOLS[index][SYMBOL_ICON]
                color = ColorPallet.GetColor(MAP_SYMBOLS[index][SYMBOL_COLOR])
                display.print(x = x + WorldMap.START_X, 
                    y = y + WorldMap.START_Y, string = icon, fg = color)