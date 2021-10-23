# Map Class, for making and using the map
# of the "world"

import tcod
import random
from ColorPallet import *
import MathFun
from Noise import *
from NameGen import *
from TownGen import *

MAP_SYMBOLS = { 
        # Acts as the "barrier" of sorts
        'Water' : ['~', "Blue", True],
        # Natural Tiles
        'Dirt' : ['.', "Brown", False],
        'Grass' : ['v', "Green", False],
        'Sand' : [chr(0x2248), "Tan", False],
        'Mountains' : ['M', "Olive", True],
        # Blocking Tiles
        'Wall' : ['#', "Grey", True],
        'Road' : [chr(0xB1), "Dark Grey", False],
        # Tiles with special actions, like flowers or portals
        'Town' : ['A', "Tristian", False],
        'Door' : ['D', 'Olive', False]
    }

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

        self.height = height
        self.curMapType = 'o'
        self.player = None
        self.mapName = GenTownName()
        self.mapID = ''
        self.width = width
        self.overworld = []
        self.towns = {}
        self.dungeons = {}
        self.noise = Noise(256)

    # Generation Techniques for the world, towns and dungeons

    def BuildOverworld(self):
        """ Builds an overworld map """
        # Size (width, height), percent chance of live cell, 
        # smoothing iterations, rebirth population, under population
        # cell_map = CellAuto.CellAuto(self.width, self.height, 45, 3, 5, 4)
        noise_map = self.noise.BuildMap(self.width, self.height, Vec2(0, 0), 23.14)

        self.overworld = []
        for row in range(self.height):
            new_row = []
            for col in range(self.width):
                if noise_map[row][col] <= -0.11:
                    new_row += ['Water']
                elif noise_map[row][col] <= -0.05:
                    new_row += ['Sand']
                elif 0.3 <= noise_map[row][col]:
                    new_row += ['Mountains']
                else:
                    if random.random() < 0.005:
                        new_row += ['Town']
                    else:
                        new_row += ['Grass']
            self.overworld += [new_row]

    def BuildTown(self, t_name, t_cord):
        """ Builds a town """
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

    # Helper functions for manipulating map functions and such

    def SetPlayer(self, player):
        """ Sets the player character for map operations """
        self.player = player

    def GetExamineAction(self):
        """ Determines the action to take when at a location when examine/use is pressed """
        s = ''
        if self.curMapType == 'o':
            index = self.overworld[self.player.Position().y][self.player.Position().x]
            # Special behaviors based on the current location
            if index == 'Town':
                t_loc = str(self.player.position.x) + ',' + str(self.player.position.y)
                if t_loc not in self.towns:
                    self.BuildTown(GenTownName(), t_loc)
                s = 'Welcome to ' + self.towns[t_loc][0][0]
                self.ChangeMap('t:' + t_loc)
                self.player.mapLoc = 't:' + t_loc
                self.player.position = Vec2(self.towns[t_loc][0][1]//2, self.towns[t_loc][0][2] - 1)
                return s
            # Everything else
            else:
                s = "You see a field of " + index
        elif self.curMapType == 't':
            pass
        elif self.curMapType == 'd':
            pass
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
        width = self.width
        height = self.height
        if self.curMapType == 't':
            width = self.towns[self.mapID][0][1]
            height = self.towns[self.mapID][0][2]
        return loc.x < 0 or loc.y < 0 or loc.x >= width or loc.y >= height
    
    def GetTownLoc(self):
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
            if cord.x < 0 or cord.x >= self.towns[self.mapID][0][1]:
                return False
            if cord.y < 0 or cord.y >= self.towns[self.mapID][0][2]:
                return False
            return MAP_SYMBOLS[self.towns[self.mapID][cord.y+1][cord.x]][2]
        elif self.curMapType == 'd':
            pass # temp place holder

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
            town_name = 'Town: ' + self.towns[self.mapID][0][0]
            display.print(x = map_display_loc.x, y = map_display_loc.y, string = town_name)
            self.DrawTown(start, display)
        if self.curMapType == 'd':
            self.DrawDungeon(start, display)

    def DrawTown(self, start : MathFun.Vec2, display : tcod.Console):
        """ Draws a town """
        # Check if the map ID is in the town index yet. It should be there from entering the town,
        # but bugs do occur
        if self.mapID not in self.towns: # Should be build upon entering, but just in case
            self.BuildTown(GenTownName(), self.mapID)
            print("Debug Warning:", self.mapID, "was not built during initial entering of town.")
        
        # Simplify the use of the repetitive data
        width = self.towns[self.mapID][0][1]
        height = self.towns[self.mapID][0][2]
        
        start.x = Clamp(0, width - WorldMap.MAP_VIEW_WIDTH, start.x)
        start.y = Clamp(0, height - WorldMap.MAP_VIEW_HEIGHT, start.y)

        for x in range(WorldMap.MAP_VIEW_WIDTH):
            for y in range(WorldMap.MAP_VIEW_HEIGHT):
                # Get the index
                index = self.towns[self.mapID][start.y + y + 1][start.x + x]
                icon = MAP_SYMBOLS[index][0]
                color = ColorLibrary.GetColor(MAP_SYMBOLS[index][1])
                display.print(x = x + WorldMap.START_X, 
                    y = y + WorldMap.START_Y, string = icon, fg = color)
        

    def DrawDungeon(self, start : MathFun.Vec2, display : tcod.Console):
        """ Draws the dungeon at a x/y coord """
        # display.print(x = 1, y = WorldMap.MAP_VIEW_HEIGHT + 3, string = "Dungeon")
        pass

    def DrawOverworld(self, start : MathFun.Vec2, display : tcod.Console):
        """ Draw Overworld (main map) to the screen """
        start.x = Clamp(0, self.width - WorldMap.MAP_VIEW_WIDTH, start.x)
        start.y = Clamp(0, self.height - WorldMap.MAP_VIEW_HEIGHT, start.y)

        for x in range(WorldMap.MAP_VIEW_WIDTH):
            for y in range(WorldMap.MAP_VIEW_HEIGHT):
                # Get the index
                index = self.overworld[start.y + y][start.x + x]
                icon = MAP_SYMBOLS[index][0]
                color = ColorLibrary.GetColor(MAP_SYMBOLS[index][1])
                display.print(x = x + WorldMap.START_X, 
                    y = y + WorldMap.START_Y, string = icon, fg = color)
